from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, String

from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel

if TYPE_CHECKING:
    from app.models.conversation import Conversation


class ContactBase(BaseSQLModel):
    bsuid: str | None = Field(
        default=None,
        sa_type=String(160),
        unique=True,
        index=True,
        nullable=True,
    )
    wa_id: str | None = Field(
        default=None,
        sa_type=String(15),
        min_length=9,
        max_length=15,
        unique=True,
        index=True,
        nullable=True,
        description="phone",
    )
    name: str | None = Field(
        sa_type=String(50), default=None, min_length=2, max_length=50
    )
    username: str | None = Field(default=None, sa_type=String(100))


class Contact(TimeStampModel, ContactBase, BaseModel, table=True):  # BD
    __tablename__ = "contacts"  # type: ignore[assignment]
    conversations: list["Conversation"] = Relationship(back_populates="contact")
