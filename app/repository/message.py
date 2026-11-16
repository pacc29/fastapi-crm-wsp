from sqlmodel import col, select

from app.common.mixins.base_repository import BaseRepository
from app.models.message import Message


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session) -> None:
        super().__init__(session, Message)

    async def get_by_wa_message_id(self, wa_message_id: str) -> Message | None:
        statement = select(Message).where(col(Message.wa_message_id) == wa_message_id)

        result = await self.session.exec(statement)

        return result.first()
