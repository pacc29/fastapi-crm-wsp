from typing import Annotated

from fastapi import APIRouter, Depends

from app.dependencies import ContactServiceDep, SessionDep, get_contact_service
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactPublic
from app.services.contact import ContactService

contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contacts_router.post("/", response_model=ContactPublic, status_code=201)
async def create_contact(
    contact_create: ContactCreate,
    service: ContactServiceDep,
):
    return await service.create_contact(contact_create)
