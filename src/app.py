"""
This module initializes the FastAPI application and includes the routes for
the application.
"""

from fastapi import FastAPI

from src.middleware.exception_handler import setup_exception_handlers
from src.middleware.http_logging import HTTPLoggingMiddleware


def create_app():
    """Create and configure the FastAPI application."""

    app = FastAPI()

    # Middlewares
    app.add_middleware(HTTPLoggingMiddleware)

    # Routes

    # Exception handling middleware
    setup_exception_handlers(app)

    return app
