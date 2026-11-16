from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.mixins.base_repository import BaseRepository
from app.models.contact import Contact


class ContactRepository(BaseRepository[Contact]):
    def __init__(
        self,
        session: AsyncSession,
    ) -> None:
        super().__init__(session, Contact)

    async def get_by_wa_id(self, wa_id: str) -> Contact | None:
        statement = select(self.model).where(self.model.wa_id == wa_id)
        result = await self.session.exec(statement)
        return result.first()

    async def get_contact_by_bsuid(self, bsuid: str) -> Contact | None:
        statement = select(self.model).where(self.model.bsuid == bsuid)
        result = await self.session.exec(statement)
        return result.first()
