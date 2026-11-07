from fastapi import APIRouter

from app.dependencies import ContactServiceDep
from app.schemas.contact import ContactCreate, ContactPublic

contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contacts_router.post("/", response_model=ContactPublic, status_code=201)
async def create_contact(
    contact_create: ContactCreate,
    service: ContactServiceDep,
):
    return await service.create_contact(contact_create)
