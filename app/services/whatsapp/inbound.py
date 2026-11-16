import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from pywa.types.others import MessageType
from pywa_async.types.message import Message as MessageAsync
from pywa_async.types.message_status import MessageStatusType
from pywa_async.types.user import User
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.enums.message import MessageDirection
from app.common.storage import build_media_path, save_file_to_path
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.media_file import MediaFile
from app.models.message import Message
from app.repository.contact import ContactRepository
from app.repository.conversation import ConversationRepository
from app.repository.media_file import MediaFileRepository
from app.repository.message import MessageRepository
from app.schemas.media_file import MediaFileCreate
from app.schemas.message import MessageCreate
from app.services.contact import ContactService
from app.services.conversation import ConversationService
from app.services.media_file import MediaFileService
from app.services.message import MessageService

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InboundContext:
    msg: MessageAsync
    contact: Contact
    conversation: Conversation

    @property
    def raw_payload(self) -> dict:
        return self.msg.raw.value

    @property
    def raw_message(self) -> dict:
        return self.raw_payload["messages"][0]

    @property
    def raw_contact(self) -> dict | None:
        contacts = self.raw_payload.get("contacts") or []
        return contacts[0] if contacts else None

    @property
    def raw_metadata(self) -> dict:
        return self.raw_payload.get("metadata", {})

    @property
    def raw_context(self) -> dict | None:
        return self.raw_message.get("context")

    @property
    def conversation_id(self) -> int:
        return self.conversation.id

    @property
    def message_type(self) -> MessageType:
        return self.msg.type


class InboundService:
    def __init__(
        self,
        contact_service: ContactService,
        conversation_service: ConversationService,
        message_service: MessageService,
        media_file_service: MediaFileService,
    ) -> None:
        self.contact_service = contact_service
        self.conversation_service = conversation_service
        self.message_service = message_service
        self.media_file_service = media_file_service

    @classmethod
    def from_session(cls, session: AsyncSession) -> "InboundService":
        return cls(
            contact_service=ContactService(ContactRepository(session)),
            conversation_service=ConversationService(ConversationRepository(session)),
            message_service=MessageService(MessageRepository(session)),
            media_file_service=MediaFileService(MediaFileRepository(session)),
        )

    def _to_message_create(self, ctx: InboundContext) -> MessageCreate:
        return MessageCreate(
            conversation_id=ctx.conversation_id,
            direction=MessageDirection.INBOUND,
            status=MessageStatusType.DELIVERED,
            wa_message_id=ctx.msg.id,
            message_type=ctx.msg.type,
            sent_at=ctx.msg.timestamp,
            delivered_at=ctx.msg.timestamp,
            data={
                "message": ctx.raw_message,
                "contact": ctx.raw_contact,
                "metadata": ctx.raw_metadata,
            },
            context=ctx.raw_context,
        )

    def _to_media_file_create(
        self,
        ctx: InboundContext,
        *,
        message_id: int,
        absolute_path: Path,
        relative_path: str,
    ) -> MediaFileCreate:
        media = ctx.msg.media

        if media is None:
            raise ValueError("Media is None")

        return MediaFileCreate(
            message_id=message_id,
            storage_path=relative_path,
            original_filename=media.filename,
            file_size=absolute_path.stat().st_size,
            mime_type=media.mime_type,
            wa_media_id=media.id,
        )

    async def _build_context(self, msg: MessageAsync) -> InboundContext:
        contact = await self._register_contact(msg.from_user)
        conversation = await self._register_conversation(contact.id, at=msg.timestamp)
        return InboundContext(msg=msg, contact=contact, conversation=conversation)

    async def _register_contact(self, user: User) -> Contact:
        return await self.contact_service.get_or_create_contact(
            bsuid=user.bsuid, wa_id=user.wa_id, name=user.name, username=user.username
        )

    async def _register_conversation(
        self, contact_id: int, *, at: datetime
    ) -> Conversation:
        return await self.conversation_service.get_or_create_active_conversation(
            contact_id, at=at
        )

    async def _register_message(self, message_create: MessageCreate) -> Message:
        return await self.message_service.create(message_create)

    async def _register_media_file(
        self, media_file_create: MediaFileCreate
    ) -> MediaFile:
        return await self.media_file_service.create(media_file_create)

    async def save_message(self, ctx: InboundContext) -> None:
        message_create = self._to_message_create(ctx)

        await self._register_message(message_create)

    async def save_audio_message(self, ctx: InboundContext) -> None:
        audio = ctx.msg.audio

        if audio is None:
            raise ValueError("Audio message is not available")

        path = build_media_path(f"inbound/{ctx.message_type}", audio.extension)

        message = await self._register_message(self._to_message_create(ctx))

        await save_file_to_path(audio.stream(), path.absolute)

        await self._register_media_file(
            self._to_media_file_create(
                ctx,
                message_id=message.id,
                absolute_path=path.absolute,
                relative_path=path.relative,
            )
        )

    async def save_image_message(self, ctx: InboundContext) -> None:
        image = ctx.msg.image

        if image is None:
            raise ValueError("Image message is not available")

        path = build_media_path(f"inbound/{ctx.message_type}", image.extension)

        message = await self._register_message(self._to_message_create(ctx))

        await save_file_to_path(image.stream(), path.absolute)

        await self._register_media_file(
            self._to_media_file_create(
                ctx,
                message_id=message.id,
                absolute_path=path.absolute,
                relative_path=path.relative,
            )
        )

    async def handle(self, msg: MessageAsync) -> None:
        if await self.message_service.get_by_wa_message_id(msg.id):
            return

        ctx = await self._build_context(msg)

        match ctx.message_type:
            case MessageType.TEXT:
                await self.save_message(ctx)
            case MessageType.AUDIO:
                await self.save_audio_message(ctx)
            case MessageType.IMAGE:
                await self.save_image_message(ctx)
            case MessageType.UNSUPPORTED:
                logger.warning(
                    "Unsupported message from %s: type=%s code=%s details=%s",
                    ctx.msg.from_user.wa_id,
                    ctx.msg.unsupported.type if ctx.msg.unsupported else None,
                    ctx.msg.error.code if ctx.msg.error else None,
                    ctx.msg.error.details if ctx.msg.error else None,
                )
                await self.save_message(ctx)
            case _:
                logger.info(
                    "No handler for message type %s from %s",
                    ctx.msg.type.value,
                    ctx.msg.from_user.wa_id,
                )
