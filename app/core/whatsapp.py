from fastapi import FastAPI
from pywa_async.client import WhatsApp

from app.core.settings import get_settings

settings = get_settings()


def create_whatsapp(app: FastAPI) -> WhatsApp:
    register_callback = settings.WHATSAPP_REGISTER_CALLBACK_URL

    if register_callback and not (
        settings.WHATSAPP_CALLBACK_URL
        and settings.WHATSAPP_APP_ID
        and settings.WHATSAPP_APP_SECRET
    ):
        raise ValueError(
            "WHATSAPP_REGISTER_CALLBACK_URL requiere WHATSAPP_CALLBACK_URL, "
            "WHATSAPP_APP_ID y WHATSAPP_APP_SECRET"
        )

    return WhatsApp(
        phone_id=settings.WHATSAPP_PHONE_ID,
        token=settings.WHATSAPP_TOKEN,
        verify_token=settings.WHATSAPP_VERIFY_TOKEN,
        server=app,
        webhook_endpoint="/webhook",
        callback_url=settings.WHATSAPP_CALLBACK_URL if register_callback else None,
        app_id=settings.WHATSAPP_APP_ID if register_callback else None,
        webhook_challenge_delay=5,
        app_secret=settings.WHATSAPP_APP_SECRET or None,
        validate_updates=(
            settings.WHATSAPP_VALIDATE_UPDATES and bool(settings.WHATSAPP_APP_SECRET)
        ),
    )
