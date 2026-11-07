from datetime import datetime
from enum import StrEnum
from typing import Any

from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import DateTime, Enum, Field, ForeignKey, String, Text

from app.common.enums.message import MessageDirection, MessageStatus, MessageType
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.types import JsonB


class MessageBase(BaseSQLModel):
    conversation_id: int = Field(ForeignKey("conversations.id"), nullable=False)
    wa_message_id: str = Field(
        sa_type=String(255), nullable=False, unique=True, max_length=255, min_length=1
    )
    direction: MessageDirection = Field(Enum(MessageDirection), nullable=False)
    status: MessageStatus = Field(Enum(MessageStatus), nullable=False)
    created_at: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    message_type: MessageType = Field(
        default=MessageType.TEXT, sa_type=Enum(MessageType), nullable=False
    )
    sent_at: datetime = Field(sa_type=DateTime(timezone=True), nullable=False)
    delivered_at: datetime = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    read_at: datetime = Field(
        default=None, sa_type=DateTime(timezone=True), nullable=True
    )
    data: JsonB | None = Field(default=None, sa_type=JSONB, nullable=True)
    context: JsonB | None = Field(default=None, sa_type=JSONB, nullable=True)


class Message(BaseModel, MessageBase, table=True):
    pass
