"""Module for application settings.

This module defines configuration settings for the application.
"""

from functools import lru_cache

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    * Implements Pydantic-Settings with validation.
    * Supports configuration over environment variables or .env-files (local development).
    * Bundles settings for all external services used in application (e.g. SAP AI Launchpad).

    Note:
        The .env file is only used and read on local development. In production, environment variables should be used.
        Values in an .env are ignored if the corresponding environment variable is already set,
        e.g., in a containerized deployment.
    """

    model_config = SettingsConfigDict(
        # env_prefix="APP_",
        env_nested_delimiter="__",
        env_file_encoding="utf-8",
        frozen=True,
        extra="ignore",
        env_file=".env",  # For local development
    )

    # General settings
    host: str = "0.0.0.0"
    port: int = 8000
    env: str = "dev"
    version: str = "0.1.0"
    app_name: str = "SAP AI Launchpad Demo Application"
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Creates a cached instance of settings.

    This function uses lru_cache to ensure that only one instance of Settings is created
    and reused throughout the application.

    Returns:
        Settings: The application settings instance.

    Note, to understand lru_cache check:
        https://docs.python.org/3/library/functools.html#functools.lru_cache
    """
    return Settings()
