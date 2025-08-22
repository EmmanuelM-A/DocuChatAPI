"""
Handles HTTP logging
"""

import time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from src.logger.default_logger import logger


class HTTPLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log incoming HTTP requests and outgoing responses.

    Logs:
    - Method and path
    - Status code
    - Request processing time
    - Optional: client IP, headers, request body (configurable)
    """

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request info
        logger.info(
            "HTTP Request | Method: %s | Path: %s | Client: %s",
            request.method,
            request.url.path,
            request.client.host if request.client else "unknown",
        )

        try:
            response: Response = await call_next(request)
        except Exception as exc:
            logger.exception("Unhandled error while processing request: %s", str(exc))
            raise

        process_time = (time.time() - start_time) * 1000  # ms

        # Log response info
        logger.info(
            "HTTP Response | Path: %s | Status: %d | Duration: %.2fms",
            request.url.path,
            response.status_code,
            process_time,
        )

        return response
