from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str
    items_per_user: int = 50
    google_api_key: str
    google_custom_search_engine: str

    model_config = SettingsConfigDict(env_file=".env")
