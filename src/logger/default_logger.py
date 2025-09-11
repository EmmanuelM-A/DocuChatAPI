"""
Logger utility for the application with colorized console output.
"""

import logging
import os
import sys
from enum import Enum
from typing import Optional

from src.config.settings import settings
from src.logger.logging_utils import LogLevel


class ColorFormatter(logging.Formatter):
    """Custom formatter to add color to log messages based on their level."""

    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, self.RESET)
        formatted_msg = super().format(record)
        return f"{color}{formatted_msg}{self.RESET}"


def __get_log_level(level: LogLevel) -> int:
    """
    Converts the log level string into its numerical counterpart.
    """

    level_mappings = {
        LogLevel.CRITICAL: 50,
        LogLevel.FATAL: 50,
        LogLevel.ERROR: 40,
        LogLevel.WARNING: 30,
        LogLevel.WARN: 30,
        LogLevel.INFO: 20,
        LogLevel.DEBUG: 10,
    }

    return level_mappings.get(level.upper(), 20)


def get_logger(
    name: str, log_dir: Optional[str] = settings.logging.LOG_DIRECTORY
) -> logging.Logger:
    """
    Returns a configured logger that logs colorized messages to the console.

    Args:
        name (str): The logger name (usually __name__).
        log_dir (Optional[str]): Directory path for logs (not used for now but
        available for extension).

    Returns:
        logging.Logger: Configured logger instance.
    """

    default_logger = logging.getLogger(name)

    log_level = __get_log_level(settings.logging.LOG_LEVEL)
    default_logger.setLevel(log_level)

    # Create formatters
    file_formatter = logging.Formatter(
        fmt=settings.logging.LOG_FORMAT,
        datefmt=settings.logging.DATE_FORMAT,
    )
    console_formatter = ColorFormatter(
        fmt=settings.logging.LOG_FORMAT,
        datefmt=settings.logging.DATE_FORMAT,
    )

    if settings.logging.IS_FILE_LOGGING_ENABLED:
        # FILE LOGGING MODE
        try:
            # Create log directory if it doesn't exist
            os.makedirs(log_dir, exist_ok=True)

            # General log file (all logs)
            app_log_path = os.path.join(log_dir, "app.log")
            file_handler = logging.FileHandler(app_log_path, encoding="utf-8")
            file_handler.setLevel(log_level)
            file_handler.setFormatter(file_formatter)
            default_logger.addHandler(file_handler)

            # Error log file (errors only)
            error_log_path = os.path.join(log_dir, "error.log")
            error_handler = logging.FileHandler(error_log_path, encoding="utf-8")
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            default_logger.addHandler(error_handler)
        except ValueError:
            # Fallback to console if file logging fails
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(console_formatter)
            default_logger.addHandler(console_handler)
    else:
        # CONSOLE LOGGING MODE
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(console_formatter)
        default_logger.addHandler(console_handler)

    return default_logger


logger = get_logger(__name__)
