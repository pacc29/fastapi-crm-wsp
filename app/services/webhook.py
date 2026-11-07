from pywa_async import filters, types
from pywa_async.client import WhatsApp


def register_handlers(wa: WhatsApp) -> None:
    @wa.on_message(filters.text)
    async def handle_message(client: WhatsApp, msg: types.Message):
        print("Received message")
        await msg.reply_text(f"Recibí: {msg.text}")
