from functools import lru_cache
from urllib.parse import quote_plus

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ENVIRONMENT: str = "local"
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_ECHO: bool = False

    WHATSAPP_PHONE_ID: str
    WHATSAPP_TOKEN: str
    WHATSAPP_VERIFY_TOKEN: str
    WHATSAPP_APP_ID: str | None = None
    WHATSAPP_APP_SECRET: str | None = None
    WHATSAPP_CALLBACK_URL: str | None = None
    WHATSAPP_REGISTER_CALLBACK_URL: bool = False
    WHATSAPP_VALIDATE_UPDATES: bool = False

    model_config = SettingsConfigDict(env_file=".env")

    @computed_field
    @property
    def database_url(self) -> str:
        return f"postgresql+psycopg://{self.DB_USER}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
