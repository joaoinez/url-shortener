import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str

    model_config = SettingsConfigDict(  # pyright: ignore[reportUnannotatedClassAttribute]
        env_file=".env"
        if os.environ.get("APP_ENV") == "production"
        else ".env.development",
        env_file_encoding="utf-8",
    )
