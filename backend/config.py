from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str | None = None
    items_per_user: int = 50
    google_api_key: str | None = None
    google_custom_search_engine: str | None = None

    model_config = SettingsConfigDict(env_file=".env")
