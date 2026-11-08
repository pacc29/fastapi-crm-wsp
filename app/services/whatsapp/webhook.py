from pywa.errors import RecipientNotInAllowedList
from pywa_async import filters
from pywa_async.client import WhatsApp
from pywa_async.types.message import Message as MessageAsync
from pywa_async.types.message_status import MessageStatusType
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.enums.message import MessageDirection
from app.db.database import async_session_factory
from app.models.contact import Contact
from app.models.conversation import Conversation
from app.models.message import Message
from app.repository.contact import ContactRepository
from app.repository.conversation import ConversationRepository
from app.services.contact import ContactService
from app.services.conversation import ConversationService


def _get_basic_info(msg: MessageAsync) -> tuple[str | None, str | None]:
    wa_id = msg.from_user.wa_id
    name = msg.from_user.name

    return (wa_id, name)


async def _register_contact(msg: MessageAsync, session: AsyncSession) -> Contact:
    wa_id, name = _get_basic_info(msg)

    if not wa_id:
        raise ValueError("wa_id is required")

    contact_service = ContactService(ContactRepository(session))
    contact = await contact_service.get_or_create_contact(phone=wa_id, name=name)

    return contact


async def _register_conversation(
    msg: MessageAsync, session: AsyncSession, contact: Contact
) -> Conversation:
    conversation_service = ConversationService(ConversationRepository(session))
    conversation = await conversation_service.get_or_create_active_conversation(
        contact.id
    )
    return conversation


async def _register_message(msg: MessageAsync, session: AsyncSession) -> None:
    wa_message_id = msg.id
    direction = MessageDirection.INBOUND
    status = MessageStatusType.DELIVERED
    message_type = msg.type
    sent_at = msg.timestamp
    data = dict(msg.__dict__)

    try:
        contact = await _register_contact(msg, session)

        conversation = await _register_conversation(msg, session, contact)

        message = Message(
            context=None,
            conversation_id=conversation.id,
            direction=direction,
            status=status,
            wa_message_id=wa_message_id,
            message_type=message_type,
            sent_at=sent_at,
            delivered_at=sent_at,
            data=data,
        )

        # message = await _register_message(msg, session, conversation)

        # return message

    except Exception:
        await session.rollback()
        raise


def register_handlers(wa: WhatsApp) -> None:
    @wa.on_message(filters.text)
    async def handle_message(client: WhatsApp, msg: MessageAsync):
        async with async_session_factory() as session:
            try:
                pass
                # contact = await _register_contact(msg, session)

            except RecipientNotInAllowedList:
                print("Recipient not in allowed list")
                raise

            except Exception:
                await session.rollback()
                raise

    @wa.on_message(filters.audio)
    async def handle_audio(client: WhatsApp, msg: MessageAsync):
        pass
