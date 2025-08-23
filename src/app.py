"""
This module initializes the FastAPI application and includes the routes for
the application.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.db_manager import get_database_manager
from src.middleware.exception_handler import setup_exception_handlers
from src.middleware.http_logging import HTTPLoggingMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown tasks."""
    db_manager = get_database_manager()

    # Startup
    await db_manager.setup_database()
    yield
    # Shutdown
    await db_manager.shutdown()


def create_app():
    """Create and configure the FastAPI application."""

    app = FastAPI(lifespan=lifespan)

    # Middlewares
    app.add_middleware(HTTPLoggingMiddleware)

    # Routes

    # Exception handling middleware
    setup_exception_handlers(app)

    return app
