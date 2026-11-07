from abc import ABC

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.common.mixins.base_model import BaseModel


class BaseRepository[T: BaseModel](ABC):
    def __init__(self, session: AsyncSession, model: type[T]) -> None:
        super().__init__()
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> T | None:
        statement = select(self.model).where(self.model.id == id)
        result = await self.session.exec(statement)
        return result.first()

    async def create(self, entity: T) -> T:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def delete(self, entity: T) -> None:
        await self.session.delete(entity)
        await self.session.flush()

    async def commit(self) -> None:
        await self.session.commit()

    async def flush(self) -> None:
        await self.session.flush()

    async def rollback(self) -> None:
        await self.session.rollback()
