from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class Settings(BaseSettings):
    DMR_BASE_URL: AnyHttpUrl
    DMR_API_KEY: str
    MODEL_ID: str
    API_BASE_URL: AnyHttpUrl | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Cache function as env settings will not change
@lru_cache
def get_settings():
    return Settings() # pyright: ignore[reportCallIssue]
