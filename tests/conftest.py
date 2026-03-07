"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient
from pydantic import SecretStr

from app.app import create_app
from app.core.config import FMCSASettings, Settings


@pytest.fixture
def settings():
    """Fixture to provide application settings for testing."""
    return Settings(
        env="test",
        version="0.1.0",
        app_name="Test App",
        api_key=SecretStr("test-api-key"),
        fmcsa=FMCSASettings(api_key=SecretStr("test-fmcsa-key")),
    )


@pytest.fixture
def client(settings: Settings):  # pylint: disable=redefined-outer-name
    """Fixture to create a TestClient for testing the FastAPI application."""
    app = create_app(settings)
    return TestClient(app)
