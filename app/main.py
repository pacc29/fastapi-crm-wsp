from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.exceptions.handlers import register_exception_handlers
from app.core.settings import get_settings
from app.core.whatsapp import create_whatsapp
from app.db.database import engine
from app.routers.contacts import contacts_router
from app.services.webhook import register_handlers

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

wa = create_whatsapp(app)
register_handlers(wa)
