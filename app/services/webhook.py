from pywa.errors import RecipientNotInAllowedList
from pywa_async import filters
from pywa_async.client import WhatsApp
from pywa_async.types.message import Message

from app.db.database import async_session_factory
from app.repository.contact import ContactRepository
from app.services.contact import ContactCreate, ContactService


def _get_basic_info(msg: Message) -> tuple[str | None, str | None]:
    wa_id = msg.from_user.wa_id
    name = msg.from_user.name

    return (wa_id, name)


def register_handlers(wa: WhatsApp) -> None:
    @wa.on_message(filters.text)
    async def handle_message(client: WhatsApp, msg: Message):
        wa_id, name = _get_basic_info(msg)

        if not wa_id:
            raise

        async with async_session_factory() as session:
            try:
                contact_service = ContactService(ContactRepository(session))
                await contact_service.create_contact(
                    ContactCreate(phone=wa_id, name=name)
                )
            except Exception:
                await session.rollback()
                raise
