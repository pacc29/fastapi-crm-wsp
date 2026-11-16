from datetime import UTC, datetime
from typing import TYPE_CHECKING

from pywa_async.types.chat import ChatType
from sqlmodel import DateTime, Enum, Field, Relationship

from app.common.enums.conversation import ConversationStatus
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel

if TYPE_CHECKING:
    from app.models.contact import Contact
    from app.models.message import Message


class ConversationBase(BaseSQLModel):
    status: ConversationStatus = Field(
        default=ConversationStatus.OPEN,
        sa_type=Enum(ConversationStatus),
        nullable=False,
    )
    last_inbound_message: datetime = Field(
        nullable=False, sa_type=DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    contact_id: int = Field(
        foreign_key="contacts.id", ondelete="CASCADE", nullable=False
    )
    chat_type: ChatType = Field(
        default=ChatType.PRIVATE, sa_type=Enum(ChatType), nullable=False
    )


class Conversation(BaseModel, ConversationBase, TimeStampModel, table=True):
    __tablename__ = "conversations" # type: ignore[assignment]
    messages: list["Message"] = Relationship(back_populates="conversation")
    contact: "Contact" = Relationship(back_populates="conversations")
