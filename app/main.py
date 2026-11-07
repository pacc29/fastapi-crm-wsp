from contextlib import asynccontextmanager

from fastapi import FastAPI
from pywa_async.client import WhatsApp

from app.core.exceptions.handlers import register_exception_handlers
from app.core.settings import get_settings
from app.db.database import engine
from app.routers.contacts import contacts_router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await engine.dispose()


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)

app.include_router(contacts_router)

wa = WhatsApp(
    phone_id=settings.WHATSAPP_PHONE_ID,
    token=settings.WHATSAPP_TOKEN,
    server=app,
    verify_token=settings.WHATSAPP_VERIFY_TOKEN,
    webhook_endpoint="/webhook",
    app_secret=settings.WHATSAPP_APP_SECRET or None,
    validate_updates=settings.WHATSAPP_VALIDATE_UPDATES
    and bool(settings.WHATSAPP_APP_SECRET),
)

from app.services import webhook  # noqa: E402, F401
