"""Authentication utilities for the HappyRobot Carrier API."""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from app.core.config import get_settings

# HappyRobot sends: Authorization: ApiKey <key>
# Swagger UI sends the raw key directly (strips the scheme)
AUTHORIZATION_HEADER = APIKeyHeader(name="Authorization", auto_error=False)


async def verify_api_key(authorization: str = Security(AUTHORIZATION_HEADER)) -> str:
    """Dependency function to verify the API key provided.

    Handles two formats:
    - HappyRobot platform: Authorization: ApiKey <key>  -> parsed, prefix stripped
    - Swagger UI:          Authorization: <key>         -> used as-is

    Args:
        authorization (str): The full Authorization header value.

    Raises:
        HTTPException: If the API key is missing or invalid.

    Returns:
        str: The valid API key.
    """
    settings = get_settings()
    expected = settings.api_key.get_secret_value()

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    # Strip "ApiKey " prefix if present (HappyRobot), otherwise use raw value (Swagger)
    scheme, _, key = authorization.partition(" ")
    api_key = key if scheme == "ApiKey" and key else authorization

    if api_key != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
