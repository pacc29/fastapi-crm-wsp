from pywa.errors import RecipientNotInAllowedList
from pywa_async import filters, types
from pywa_async.client import WhatsApp


def register_handlers(wa: WhatsApp) -> None:
    @wa.on_message(filters.text)
    async def handle_message(client: WhatsApp, msg: types.Message):
        try:
            await msg.reply_text(f"Recibí: {msg.text}")
        except RecipientNotInAllowedList:
            print("El destinatario %s no está en la lista permitida del número de prueba", msg.from_user.wa_id)