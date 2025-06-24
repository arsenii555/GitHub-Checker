"""Read .env."""
import typing
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("ScrapperSettings",)


class ScrapperSettings(BaseSettings):
    """Scrapper settings."""

    bot_url: str = Field(...)
    scrapper_url: str = Field(...)
    github_api_key: str = Field(...)

    model_config: typing.ClassVar[SettingsConfigDict] = SettingsConfigDict(
        extra="ignore",
        frozen=True,
        case_sensitive=False,
        env_file=Path(__file__).parent.parent / ".env",
        env_prefix="SCRAPPER_",
    )
