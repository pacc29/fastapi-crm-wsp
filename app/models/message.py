from datetime import datetime
from typing import TYPE_CHECKING

from pywa.types.others import MessageType
from pywa_async.types.message_status import MessageStatusType
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import DateTime, Enum, Field, Relationship, String

from app.common.enums.message import MessageDirection
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.types import JsonB

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class MessageBase(BaseSQLModel):
    conversation_id: int = Field(foreign_key="conversations.id", nullable=False)
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
    read_at: datetime | None = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    data: JsonB | None = Field(default=None, sa_type=JSONB(none_as_null=True), nullable=True)
    context: JsonB | None = Field(default=None, sa_type=JSONB(none_as_null=True), nullable=True)


class Message(BaseModel, MessageBase, table=True):
    __tablename__ = "messages" # type: ignore[assignment]
    conversation: "Conversation" = Relationship(back_populates="messages")
