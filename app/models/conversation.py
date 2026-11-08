from datetime import datetime

from pywa_async.types.chat import ChatType
from sqlmodel import DateTime, Enum, Field, ForeignKey, Relationship

from app.common.enums.conversation import ConversationStatus
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel
from app.models.contact import Contact


class ConversationBase(BaseSQLModel):
    status: ConversationStatus = Field(
        default=ConversationStatus.OPEN,
        sa_type=Enum(ConversationStatus),
        nullable=False,
    )
    last_inbound_message: datetime = Field(
        nullable=False, sa_type=DateTime(timezone=True), default=datetime.now()
    )
    contact_id: int = Field(
        ForeignKey("contacts.id", ondelete="CASCADE"), nullable=False
    )
    chat_type: ChatType = Field(
        default=ChatType.PRIVATE, sa_type=Enum(ChatType), nullable=False
    )


class Conversation(BaseModel, ConversationBase, TimeStampModel, table=True):
    contact: Contact = Relationship(back_populates="conversations")
