from app.models.conversation import Conversation
from app.repository.conversation import ConversationRepository


class ConversationService:
    def __init__(self, conversation_repository: ConversationRepository) -> None:
        self.conversation_repository = conversation_repository

    async def _close_expired_conversations(self) -> None:
        await self.conversation_repository.close_expired_conversations()

    async def get_active_conversation(self, contact_id: int) -> Conversation | None:
        await self._close_expired_conversations()
        conversation = await self.conversation_repository.get_active_conversation(
            contact_id
        )

        return conversation

    async def create_conversation(self, contact_id: int) -> Conversation:
        conversation = await self.conversation_repository.create(
            Conversation(contact_id=contact_id)
        )

        return conversation

    async def get_or_create_active_conversation(self, contact_id: int) -> Conversation:
        conversation = await self.get_active_conversation(contact_id)
        if conversation:
            return conversation
        return await self.create_conversation(contact_id)
