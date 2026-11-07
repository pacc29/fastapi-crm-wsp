from datetime import datetime

from sqlmodel import DateTime, Enum, Field

from app.common.enums.conversation import ConversationStatus
from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel


class ConversationBase(BaseSQLModel):
    status: ConversationStatus = Field(
        default=ConversationStatus.OPEN,
        sa_type=Enum(ConversationStatus),
        nullable=False,
    )
    last_inbound_message: datetime = Field(
        nullable=False, sa_type=DateTime(timezone=True)
    )


class Conversation(BaseModel, ConversationBase, TimeStampModel, table=True):
    pass
