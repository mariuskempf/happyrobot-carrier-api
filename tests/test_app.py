"""Tests for the FastAPI application."""


def test_health_returns_200(client):
    """Test that the /health endpoint returns a 200 status code."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_body(client, settings):
    """Test that the /health endpoint returns the expected response body."""
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == settings.version
    assert data["env"] == settings.env
