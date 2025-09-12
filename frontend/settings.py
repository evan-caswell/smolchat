from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DMR_BASE_URL: str | None = None
    DMR_API_KEY: str | None = None
    MODEL_ID: str
    API_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Load frontend settings from environment (cached)."""
    return Settings()  # pyright: ignore[reportCallIssue]

settings = get_settings()
