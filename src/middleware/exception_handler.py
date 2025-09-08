"""
Global exception handler for structured error responses and logging.
Handles both custom ApiException instances and unexpected errors.
"""

from fastapi import Request, HTTPException, status, FastAPI
from starlette.responses import JSONResponse

from src.logger.default_logger import logger
from src.utils.api_exceptions import ApiException
from src.utils.api_responses import ErrorDetail, ErrorResponse


async def api_exception_handler(request: Request, exc: ApiException) -> JSONResponse:
    """
    Handle all exceptions derived from ApiException (custom application errors).
    """

    # TODO: MAKE A DEV_LOG_FORMAT AND PROD_LOG_FORMAT
    logger.error(
        "API Exception | Path: %s | Status Code: %d | Error Code: %s | Details: %s",
        request.url.path,
        exc.status_code,
        exc.error_detail.code,
        exc.error_detail.details or exc.message,
    )

    return ErrorResponse(
        error=exc.error_detail, message=exc.message, status_code=exc.status_code
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI's native HTTPException errors.
    """

    error_detail = ErrorDetail(
        code="HTTP_EXCEPTION",
        details=str(exc.detail),
    )

    logger.warning(
        "HTTPException | Path: %s | Status: %d | Detail: %s",
        request.url.path,
        exc.status_code,
        exc.detail,
    )

    return ErrorResponse(
        error=error_detail,
        message="A request error occurred.",
        status_code=exc.status_code,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Catch-all handler for unexpected runtime exceptions.
    """
    error_detail = ErrorDetail(
        code="INTERNAL_SERVER_ERROR",
        details=str(exc),
    )

    logger.exception(
        "Unhandled Exception | Path: %s | Error: %s",
        request.url.path,
        str(exc),
    )

    return ErrorResponse(
        error=error_detail,
        message="An unexpected error occurred.",
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """Registers exception handlers to the application."""

    app.add_exception_handler(ApiException, api_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_exception_handler)
