from datetime import datetime, timedelta

from sqlmodel import col, select, update

from app.common.enums.conversation import ConversationStatus
from app.common.mixins.base_repository import BaseRepository
from app.models.conversation import Conversation


class ConversationRepository(BaseRepository[Conversation]):
    def __init__(self, session):
        super().__init__(session, Conversation)

    async def close_expired_conversations(self) -> None:
        statement = (
            update(Conversation)
            .where(
                col(Conversation.status) == ConversationStatus.OPEN,
                col(Conversation.last_inbound_message)
                <= datetime.now() - timedelta(hours=24),
            )
            .values(status=ConversationStatus.CLOSED)
        )

        await self.session.exec(statement)
        await self.session.commit()

    async def get_active_conversation(self, contact_id: int) -> Conversation | None:
        statement = select(Conversation).where(
            col(Conversation.contact_id) == contact_id,
            col(Conversation.status) == ConversationStatus.OPEN,
        )

        result = await self.session.exec(statement)

        return result.first()