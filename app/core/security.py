"""Authentication utilities for the HappyRobot Carrier API."""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(api_key: str = Security(API_KEY_HEADER)) -> str:
    """Dependency that validates the X-API-Key header.

    To be injected into any route or router that requires authentication.

    Args:
        api_key (str, optional): The API key extracted from the X-API-Key header.
            Defaults to None if the header is missing.

    Raises:
        HTTPException: If the API key is missing or invalid.

    Returns:
        str: The valid API key.
    """
    settings = get_settings()

    if not api_key or api_key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
