"""Authentication utilities for the HappyRobot Carrier API."""

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, APIKeyQuery

from app.core.config import get_settings

API_KEY_QUERY = APIKeyQuery(name="api_key", auto_error=False)
API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


async def verify_api_key(
    api_key_header: str = Security(API_KEY_HEADER),
    api_key_query: str = Security(API_KEY_QUERY),
) -> str:
    """Dependency function to verify the API key provided.

    Note: It checks for the API key in either the X-API-Key header or
    the api_key query parameter.

    Args:
        api_key_header (str): The API key provided in the X-API-Key header.
        api_key_query (str): The API key provided in the api_key query parameter.

    Raises:
        HTTPException: If the API key is missing or invalid.

    Returns:
        str: The valid API key.
    """
    settings = get_settings()

    api_key = api_key_header or api_key_query

    print(api_key)
    print(settings.api_key.get_secret_value())

    if not api_key or api_key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
            headers={"WWW-Authenticate": "ApiKey"},
        )
    return api_key
