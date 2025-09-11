"""
Responsible for defining the models used to log data.
"""

import datetime as dt
from typing import Optional, Any

# TODO: ADD MORE ROBUST LOGGING FOR THE DATABASE

from pydantic import BaseModel, Field

from src.logger.logging_utils import LogLevel


class LogFormat(BaseModel):
    """The base format for all logs."""

    timestamp: dt.datetime = Field(
        default_factory=lambda: dt.datetime.now(dt.timezone.utc),
        description="UTC timestamp when the log was recorded.",
    )

    level: LogLevel = Field(description="The severity level of the log message.")

    message: str = Field(description="The descriptive message for the log event.")


class DatabaseLogFormat(LogFormat):
    """Base pydantic model for all database and database related logs"""

    db_action: Optional[str] = Field(
        default=None,
        description="The action performed on the database (e.g., connect, query, migrate).",
    )

    additional: Optional[dict[str, Any]] = Field(
        default=None, description="The additional data associated with the log."
    )


class DatabaseStandardLog(DatabaseLogFormat):
    """Pydantic model for data for all non-error logs"""


class DatabaseErrorLog(DatabaseLogFormat):
    """Pydantic model for all error/warning logs"""

    source_file: Optional[str] = Field(
        default=None, description="The file where the log originated."
    )

    exception: Optional[str] = Field(
        default=None, description="Exception name if the log relates to an error."
    )

    traceback: Optional[str] = Field(
        default=None, description="Full traceback string for debugging critical errors."
    )
