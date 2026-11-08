from pydantic import ConfigDict
from sqlmodel import Field, SQLModel


class BaseSQLModel(SQLModel):
    model_config = ConfigDict(str_strip_whitespace=True, from_attributes=True)


class BaseModel(BaseSQLModel):
    id: int = Field(default=None, primary_key=True)
