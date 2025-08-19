"""
This module initializes the FastAPI application and includes the routes for
the application.
"""

from fastapi import FastAPI

from src.middleware.exception_handler import setup_exception_handlers


def create_app():
    """Create and configure the FastAPI application."""

    app = FastAPI()

    # Register routes

    setup_exception_handlers(app)

    return app
