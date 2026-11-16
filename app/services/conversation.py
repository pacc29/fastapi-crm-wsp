from datetime import datetime

from app.models.conversation import Conversation
from app.repository.conversation import ConversationRepository


class ConversationService:
    def __init__(self, conversation_repository: ConversationRepository) -> None:
        self.conversation_repository = conversation_repository

    async def _close_expired_conversations(self) -> None:
        await self.conversation_repository.close_expired_conversations()

    async def get_active_conversation(self, contact_id: int) -> Conversation | None:
        await self._close_expired_conversations()
        return await self.conversation_repository.get_active_conversation(contact_id)

    async def create(self, contact_id: int, *, at: datetime) -> Conversation:
        return await self.conversation_repository.create(
            Conversation(contact_id=contact_id, last_inbound_message=at)
        )

    async def get_or_create_active_conversation(
        self, contact_id: int, *, at: datetime
    ) -> Conversation:
        conversation = await self.get_active_conversation(contact_id)

        if conversation is None:
            return await self.create(contact_id, at=at)

        if at > conversation.last_inbound_message:
            conversation.last_inbound_message = at
            return await self.conversation_repository.update(conversation)

        return conversation
