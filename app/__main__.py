"""Main entry point for the Inbound Carrier Sales Demo Application."""

import uvicorn

from app.app import create_app
from app.core.config import get_settings

settings = get_settings()

application = create_app(settings=settings)

if __name__ == "__main__":
    # Run the application with Uvicorn ASGI server
    uvicorn.run(
        app=application,
        host=settings.host,
        port=settings.port,
        log_config=None,
        log_level=None,
    )
