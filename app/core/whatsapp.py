from pywa_async.client import WhatsApp

from app.core.settings import get_settings

settings = get_settings()

wa = WhatsApp(
    phone_id=settings.WHATSAPP_PHONE_ID,
    token=settings.WHATSAPP_TOKEN,
    verify_token=settings.WHATSAPP_VERIFY_TOKEN,
    webhook_endpoint="/webhook",
    app_secret=settings.WHATSAPP_APP_SECRET or None,
    validate_updates=(
        settings.WHATSAPP_VALIDATE_UPDATES and bool(settings.WHATSAPP_APP_SECRET)
    ),
)
