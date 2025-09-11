"""
Contains logging utils used only for logging purposes.
"""

from enum import Enum


class LogLevel(str, Enum):
    """All possible log levels a logger can take."""

    CRITICAL = "CRITICAL"
    FATAL = "FATAL"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"
