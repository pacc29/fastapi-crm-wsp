
from app.common.mixins.base_repository import BaseRepository
from app.models.message import Message


class MessageRepository(BaseRepository[Message]):
    def __init__(self, session) -> None:
        super().__init__(session, Message)

    
    