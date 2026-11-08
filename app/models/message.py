from datetime import datetime

from pywa.types.others import MessageType
from pywa_async.types.message_status import MessageStatusType
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import DateTime, Enum, Field, ForeignKey, String

from app.common.enums.message import MessageDirection
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.types import JsonB


class MessageBase(BaseSQLModel):
    conversation_id: int = Field(ForeignKey("conversations.id"), nullable=False)
    wa_message_id: str = Field(
        sa_type=String(255), nullable=False, unique=True, max_length=255, min_length=1
    )
    direction: MessageDirection = Field(Enum(MessageDirection), nullable=False)
    status: MessageStatusType = Field(Enum(MessageStatusType), nullable=False)
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True), nullable=False, default=datetime.now()
    )
    message_type: MessageType = Field(
        default=MessageType.TEXT, sa_type=Enum(MessageType), nullable=False
    )
    sent_at: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    delivered_at: datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    read_at: datetime = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    data: JsonB | None = Field(default=None, sa_type=JSONB, nullable=True)
    context: JsonB | None = Field(default=None, sa_type=JSONB, nullable=True)


class Message(BaseModel, MessageBase, table=True):
    pass
