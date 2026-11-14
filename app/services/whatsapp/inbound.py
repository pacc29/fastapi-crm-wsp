from fastapi import HTTPException
from pywa.types.others import MessageType
from pywa_async.types.message import Message as MessageAsync
from pywa_async.types.message_status import MessageStatusType
from pywa_async.types.user import User
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.enums.message import MessageDirection
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message
from app.repository.contact import ContactRepository
from app.repository.conversation import ConversationRepository
from app.repository.message import MessageRepository
from app.schemas.message import MessageCreate
from app.services.contact import ContactService
from app.services.conversation import ConversationService
from app.services.message import MessageService


class InboundService:
    def __init__(
        self,
        contact_service: ContactService,
        conversation_service: ConversationService,
        message_service: MessageService,
    ) -> None:
        self.contact_service = contact_service
        self.conversation_service = conversation_service
        self.message_service = message_service

    @classmethod
    def from_session(cls, session: AsyncSession) -> "InboundService":
        return cls(
            contact_service=ContactService(ContactRepository(session)),
            conversation_service=ConversationService(ConversationRepository(session)),
            message_service=MessageService(MessageRepository(session)),
        )

    def _get_basic_info(self, user: User) -> tuple[str | None, str | None]:
        wa_id = user.wa_id
        name = user.name
        return (wa_id, name)

    async def _register_contact(self, user: User) -> Contact:
        wa_id, name = self._get_basic_info(user)

        if not wa_id:
            raise HTTPException(status_code=400, detail="wa_id is required")

        contact = await self.contact_service.get_or_create_contact(
            phone=wa_id, name=name
        )
        return contact

    async def _register_conversation(self, contact_id: int) -> Conversation:
        conversation = (
            await self.conversation_service.get_or_create_active_conversation(
                contact_id
            )
        )
        return conversation

    async def _register_message(self, message_create: MessageCreate) -> Message:
        return await self.message_service.create_message(message_create)

    async def save_text_message(self, msg: MessageAsync, conversation_id: int) -> None:
        raw_message: dict = msg.raw.value["messages"][0]
        await self._register_message(
            MessageCreate(
                context=None,
                conversation_id=conversation_id,
                direction=MessageDirection.INBOUND,
                status=MessageStatusType.DELIVERED,
                wa_message_id=msg.id,
                message_type=msg.type,
                sent_at=msg.timestamp,
                delivered_at=msg.timestamp,
                data=raw_message,
            )
        )

    async def handle(self, msg: MessageAsync) -> None:
        contact = await self._register_contact(msg.from_user)
        conversation = await self._register_conversation(contact.id)

        match msg.type:
            case MessageType.TEXT:
                await self.save_text_message(msg, conversation.id)
