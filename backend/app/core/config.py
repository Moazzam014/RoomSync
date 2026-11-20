
from typing import Literal

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    TEST_DATABASE_URL: str | None = None

    APP_NAME: str = "RoomSync"
    APP_ENV: Literal["development", "test", "production"] = "development"

    # Debug is disabled unless explicitly enabled in the environment.
    DEBUG: bool = False

    # Comma-separated frontend origins.
    CORS_ORIGINS: str = (
        "http://localhost:5173,"
        "http://127.0.0.1:5173"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @property
    def cors_origins(self) -> list[str]:
        return [
            origin.strip().rstrip("/")
            for origin in self.CORS_ORIGINS.split(",")
            if origin.strip()
        ]

    @model_validator(mode="after")
    def validate_production_settings(self):
        if self.APP_ENV == "production":
            if self.DEBUG:
                raise ValueError(
                    "DEBUG must be false in production."
                )

            if len(self.SECRET_KEY) < 32:
                raise ValueError(
                    "Production SECRET_KEY must contain "
                    "at least 32 characters."
                )

            if "*" in self.cors_origins:
                raise ValueError(
                    "Wildcard CORS origins are not allowed "
                    "in production."
                )

        return self


settings = Settings()
