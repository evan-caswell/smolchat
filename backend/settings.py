from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DMR_BASE_URL: str
    DMR_API_KEY: str
    MODEL_ID: str
    API_BASE_URL: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Load settings from environment (cached for process lifetime)."""
    return Settings()  # pyright: ignore[reportCallIssue]

settings = get_settings()
