"""
Logger utility for the application with colorized console output.
"""

import logging
import os
from typing import Optional

from src.config.settings import settings


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


def get_logger(
    name: str, log_dir: Optional[str] = settings.LOG_DIRECTORY
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

    if default_logger.hasHandlers():
        return default_logger  # Avoid adding multiple handlers

    # Set global level TODO: switch to env-controlled later
    default_logger.setLevel(logging.DEBUG)

    # Create log directory (no file handlers yet, but future-proof)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)

    # Colorized console handler
    console_handler = logging.StreamHandler()
    color_formatter = ColorFormatter(
        fmt="[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(color_formatter)
    default_logger.addHandler(console_handler)

    return default_logger


logger = get_logger(__name__)
