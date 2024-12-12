from functools import lru_cache

from pydantic import EmailStr, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "Awesome 2API"
    admin_email: EmailStr
    items_per_user: int = 50
    google_api_key: str
    google_custom_search_engine: str
    mail_server: str | None = None
    mail_username: str | None = None
    mail_password: SecretStr = "strong_password"
    mail_from: EmailStr

    model_config = SettingsConfigDict(env_file=".env")
