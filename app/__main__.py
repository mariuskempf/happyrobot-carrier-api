"""Main entry point for the Inbound Carrier Sales Demo Application."""

import uvicorn

from app.app import create_app
from app.core.config import get_settings
from app.core.log import setup_logging

settings = get_settings()

setup_logging(log_level=settings.log_level)

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
