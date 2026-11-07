from contextlib import asynccontextmanager

from fastapi import FastAPI
from pywa_async.client import WhatsApp

from app.core.exceptions.handlers import register_exception_handlers
from app.db.database import engine
from app.routers.contacts import contacts_router


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
    phone_id="1489769414212299",
    token="EAAjvIOZBnTFsBS8Kc8ZBlM98ZBPFJdq2QfGpWq2YNKBVedv4tq1fzQn69m9Nf3UMd6AC4L0h6ZAqspVK5egbbV2pcQT8HYFQGUwPabLvec28GDq1uGZCFbytFdwzZAPPSB21UM1HPQSsAjyR2az81kduX5T6xezeOFO6pnjIzfgzXZCssa4Ks7zPyZAZBBq1uj2dlMnoIMdgfiuPRtlAA9kRFJASGNioFbJGkxYmZC85ZA0z85RWUjFt9i95kal2BRFt6ImQbMwpOfsJLaj2691FEU7",
    server=app,
    verify_token="1234567890",
    webhook_endpoint="/webhook",
    validate_updates=False,
)
