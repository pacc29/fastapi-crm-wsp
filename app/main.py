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
    token="EAAjvIOZBnTFsBS1u3ilKhKyzmzZCpRRTpks3Udu6WiqQ8pRCCTZA56OZCyBZCjXvCTgLGlbBBzLqSJmZCRFiKrhHzomRYjMRGsnklmw4fZCGEPissDI4V231H23HzfH3T1MDg55HPTnZB7ZB5UgYuXjaOsQ62cRlnVF66OpumwdTM3whHC2BgDLWxf20WZC8AheD3OMrGFn7O2SCQfKSKHwoIwZAugQDTVIBGgkwuTMQOk7foVzh3ZAx2LSF2oALRI278TyPw83JB7pi0I3OhIPRhiK9",
    server=app,
    verify_token="1234567890",
    webhook_endpoint="/webhook",
    validate_updates=False,
)
