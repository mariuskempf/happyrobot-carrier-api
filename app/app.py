"""Main application setup for the HappyRobot Carrier API."""

from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import Settings
from app.core.security import verify_api_key
from app.routers import demo

# from app.routers import calls, carriers, loads, negotiation


@asynccontextmanager
async def lifespan(app: FastAPI):  # pylint: disable=unused-argument
    """Lifespan context manager for application startup and shutdown events.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    logger.info("Starting FastApi application")

    yield

    # Shutdown
    logger.info("Shutting down...")


def create_app(settings: Settings) -> FastAPI:
    """Factory function to create and configure the FastAPI application instance.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """

    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        description="Backend API for the HappyRobot inbound carrier load sales agent.",
        lifespan=lifespan,
        # Disable docs in production
        docs_url="/docs" if settings.env == "dev" else None,
        redoc_url="/redoc" if settings.env == "dev" else None,
    )

    # --- Middleware ---
    # Note: CORS is configured to allow all origins, methods, and headers for simplicity in this demo application.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Routers ---
    # All business routes are protected by API key auth

    # app.include_router(carriers.router, prefix="/carriers", tags=["Carriers"], **protected)
    # app.include_router(loads.router, prefix="/loads", tags=["Loads"], **protected)
    # app.include_router(negotiation.router, prefix="/negotiation", tags=["Negotiation"], **protected)
    # app.include_router(calls.router, prefix="/calls", tags=["Calls"], **protected)
    app.include_router(demo.router, prefix="/demo", tags=["Demo"], dependencies=[Depends(verify_api_key)])

    # Health check — intentionally unprotected so HappyRobot can ping it
    @app.get("/health", tags=["Observability"])
    def health():
        """Health check endpoint."""
        return {
            "status": "ok",
            "version": settings.version,
            "env": settings.env,
        }

    @app.get("/health", tags=["Observability"])
    def ready():
        """Readiness check endpoint."""
        return {
            "status": "ok",
            "version": settings.version,
            "env": settings.env,
        }

    return app
