from datetime import datetime

from pydantic import ConfigDict
from sqlmodel import Field

from app.common.mixins.base_model import BaseSQLModel
from app.models.contact import ContactBase


class ContactCreate(ContactBase):  # request POST
    pass


class ContactPublic(ContactBase):  # response
    id: int
    created_at: datetime


class ContactUpdate(BaseSQLModel):  # request PATCH
    model_config = ConfigDict(extra="forbid")
    phone: str | None = Field(default=None, min_length=9, max_length=15)
    name: str | None = Field(default=None, min_length=2, max_length=50)
