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

    async def get_by_phone(self, phone: str) -> Contact | None:
        statement = select(self.model).where(self.model.phone == phone)
        result = await self.session.exec(statement)
        return result.first()
