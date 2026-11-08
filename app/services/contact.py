from app.models.contact import Contact
from app.repository.contact import ContactRepository
from app.schemas.contact import ContactCreate


class ContactService:
    def __init__(self, contact_repository: ContactRepository) -> None:
        self.contact_repository = contact_repository

    async def _get_contact_by_phone(self, phone: str):
        return await self.contact_repository.get_by_phone(phone)

    async def create_contact(self, contact_create: ContactCreate) -> Contact:
        contact = Contact.model_validate(contact_create)
        await self.contact_repository.create(contact)
        return contact

    async def get_or_create_contact(self, phone: str, name: str | None) -> Contact:
        contact = await self._get_contact_by_phone(phone)
        if contact:
            return contact
        return await self.create_contact(ContactCreate(phone=phone, name=name))
