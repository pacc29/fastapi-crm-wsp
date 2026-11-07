import pywa_async.types.message as types
from pywa_async import filters
from pywa_async.client import WhatsApp

from app.main import wa


@wa.on_message(filters.text)
async def handle_message(client: WhatsApp, msg: types.Message):
    print("Recieved message")
    await msg.reply_text(f"Recibí: {msg.text}")
