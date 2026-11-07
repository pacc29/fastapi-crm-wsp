from typing import Annotated

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import Settings, get_settings
from app.db.database import get_session
from app.repository.contact import ContactRepository
from app.services.contact import ContactService

SessionDep = Annotated[AsyncSession, Depends(get_session)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_contact_service(
    session: SessionDep,
) -> ContactService:
    return ContactService(contact_repository=ContactRepository(session))


ContactServiceDep = Annotated[ContactService, Depends(get_contact_service)]
