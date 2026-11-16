from app.models.contact import Contact
from app.repository.contact import ContactRepository
from app.schemas.contact import ContactCreate


class ContactService:
    def __init__(self, contact_repository: ContactRepository) -> None:
        self.contact_repository = contact_repository

    async def _get_contact_by_wa_id(self, wa_id: str):
        return await self.contact_repository.get_by_wa_id(wa_id)

    async def _get_contact_by_bsuid(self, bsuid: str):
        return await self.contact_repository.get_contact_by_bsuid(bsuid)

    async def create(self, contact_create: ContactCreate) -> Contact:
        contact = Contact.model_validate(contact_create)
        await self.contact_repository.create(contact)
        return contact

    async def get_or_create_contact(
        self, *, bsuid: str, wa_id: str | None, name: str | None, username: str | None
    ) -> Contact:
        contact = await self._get_contact_by_bsuid(bsuid)

        if contact:
            changed = False
            for field, value in (
                ("wa_id", wa_id),
                ("name", name),
                ("username", username),
            ):
                if value and getattr(contact, field) != value:
                    setattr(contact, field, value)
                    changed = True

            if changed:
                contact = await self.contact_repository.update(contact)

            return contact

        return await self.create(
            ContactCreate(bsuid=bsuid, wa_id=wa_id, name=name, username=username)
        )
