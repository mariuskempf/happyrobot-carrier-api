"""Shared pytest fixtures."""

import pytest
from fastapi.testclient import TestClient

from app.app import create_app
from app.core.config import Settings


@pytest.fixture
def settings():
    """Fixture to provide application settings for testing."""
    return Settings(env="test", version="0.1.0", app_name="Test App")


@pytest.fixture
def client(settings: Settings):  # pylint: disable=redefined-outer-name
    """Fixture to create a TestClient for testing the FastAPI application."""
    app = create_app(settings)
    return TestClient(app)
