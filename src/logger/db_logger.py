"""
Responsible for logging database related operations.
"""

import logging
import datetime as dt
import os
import sys
from pathlib import Path
from typing import Type

from pydantic import BaseModel
from sqlalchemy.testing.config import ident

from src.config.settings import settings
from src.logger.default_logger import ColorFormatter, get_log_level
from src.logger.log_format import (
    DatabaseLogFormat,
    DatabaseStandardLog,
    DatabaseErrorLog,
)


class JSONFormatter(logging.Formatter):
    """Formatter that outputs logs as JSON using Pydantic models."""

    def __init__(self, model: Type[BaseModel] = DatabaseLogFormat):
        super().__init__()
        self.model = model

    def format(self, record: logging.LogRecord) -> str:
        log_dict = {
            "timestamp": dt.datetime.now(dt.timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key not in log_dict and not key.startswith("_"):
                log_dict[key] = value

        structured = self.model(**log_dict)
        return structured.model_dump_json(indent=4)


def get_logger(name: str, model: Type[BaseModel]) -> logging.Logger:
    """
    Returns a configured logger that logs colorized messages to the console
    and structured JSON logs to files.

    Args:
        name: The logger name.
        model: The Pydantic log format model.

    Returns:
        logging.Logger: Configured logger instance.
    """

    logger = logging.getLogger(name)
    log_level = get_log_level(settings.logging.LOG_LEVEL)
    logger.setLevel(log_level)
    logger.propagate = False

    log_dir = settings.database.DB_LOG_DIR

    # Clear old handlers to allow reconfiguring with different models
    if logger.handlers:
        logger.handlers.clear()

    # Formatters
    file_formatter = JSONFormatter(model=model)
    console_formatter = ColorFormatter(
        fmt=settings.logging.CONSOLE_LOG_FORMAT,
        datefmt=settings.logging.DATE_FORMAT,
    )

    try:
        os.makedirs(log_dir, exist_ok=True)

        # File output → structured JSON
        file_handler = logging.FileHandler(
            os.path.join(log_dir, "app.log"), encoding="utf-8"
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Error file → errors only, structured JSON
        error_handler = logging.FileHandler(
            os.path.join(log_dir, "error.log"), encoding="utf-8"
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(file_formatter)
        logger.addHandler(error_handler)
    except (OSError, ValueError):
        # Fallback to console only if file logging fails
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
