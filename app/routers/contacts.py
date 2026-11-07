from fastapi import APIRouter

from app.dependencies import SessionDep
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactPublic

contacts_router = APIRouter(prefix="/contacts", tags=["Contacts"])


@contacts_router.post("/", response_model=ContactPublic, status_code=201)
async def create_contact(contact_create: ContactCreate, session: SessionDep):
    contact = Contact.model_validate(contact_create)
    session.add(contact)
    await session.commit()
    return contact
