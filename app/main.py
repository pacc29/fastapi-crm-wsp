from contextlib import asynccontextmanager

from fastapi import FastAPI

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
