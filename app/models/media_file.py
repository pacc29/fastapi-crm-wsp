from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, String

from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel

if TYPE_CHECKING:
    from app.models.message import Message


class MediaFileBase(BaseSQLModel):
    message_id: int = Field(
        foreign_key="messages.id", ondelete="CASCADE", nullable=False, unique=True
    )
    storage_path: str = Field(
        sa_type=String(255), max_length=255, nullable=False, unique=True
    )
    original_filename: str | None = Field(
        default=None, sa_type=String(255), nullable=True
    )
    file_size: int = Field(nullable=False)
    mime_type: str = Field(sa_type=String(100), max_length=100, nullable=False)
    wa_media_id: str = Field(sa_type=String(255), max_length=255, nullable=False)


class MediaFile(BaseModel, MediaFileBase, TimeStampModel, table=True):
    __tablename__ = "media_files"  # type: ignore[assignment]
    message: "Message" = Relationship(back_populates="media_file")
    
