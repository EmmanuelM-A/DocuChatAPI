"""
This module initializes the FastAPI application and includes the routes for
the application.
"""

from fastapi import FastAPI


def create_app():
    """Create and configure the FastAPI application."""

    app = FastAPI()

    # Register routes

    # Global error handling
    # app.add_exception_handler(ApiException)

    return app
