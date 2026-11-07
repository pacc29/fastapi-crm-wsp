from sqlmodel import Field, String

from app.common.mixins.base_model import BaseModel, BaseSQLModel
from app.common.mixins.timestamp_model import TimeStampModel


class ContactBase(BaseSQLModel):
    phone: str = Field(
        sa_type=String(15), min_length=9, max_length=15, unique=True, index=True
    )
    name: str | None = Field(
        sa_type=String(50), default=None, min_length=2, max_length=50
    )


class Contact(TimeStampModel, ContactBase, BaseModel, table=True):  # BD
    pass
