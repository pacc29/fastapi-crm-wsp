from pywa_async.client import WhatsApp
from pywa_async.types.message import Message as MessageAsync

from app.db.database import session_scope
from app.services.whatsapp.inbound import InboundService


def register_handlers(wa: WhatsApp) -> None:
    @wa.on_message()
    async def handle_message(client: WhatsApp, msg: MessageAsync):
        async with session_scope() as session:
            await InboundService.from_session(session).handle(msg)
