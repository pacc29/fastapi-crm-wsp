from fastapi import FastAPI
from pywa_async.client import WhatsApp

from app.core.settings import get_settings

settings = get_settings()


def create_whatsapp(app: FastAPI) -> WhatsApp:
    return WhatsApp(
        phone_id=settings.WHATSAPP_PHONE_ID,
        token=settings.WHATSAPP_TOKEN,
        verify_token=settings.WHATSAPP_VERIFY_TOKEN,
        server=app,
        webhook_endpoint="/webhook",
        app_id=settings.WHATSAPP_APP_ID,
        app_secret=settings.WHATSAPP_APP_SECRET,
        validate_updates=settings.WHATSAPP_VALIDATE_UPDATES,
    )
