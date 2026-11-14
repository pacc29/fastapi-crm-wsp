from app.models.message import Message
from app.repository.message import MessageRepository
from app.schemas.message import MessageCreate


class MessageService:
    def __init__(self, message_repository: MessageRepository) -> None:
        self.message_repository = message_repository

    async def create_message(self, message_create: MessageCreate) -> Message:
        message = Message.model_validate(message_create)
        return await self.message_repository.create(message)
