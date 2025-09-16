"""
Database logger
"""

import json
import logging
from pathlib import Path
from typing import Optional

from src.config.settings import settings
from src.logger.log_format import DatabaseStandardLog, DatabaseErrorLog
from src.logger.logging_utils import LogLevel

# TODO: USE THE DATABASE LOGGER IN THE DATABASE LAYER INSTEAD OF THE REGULAR LOGGER


def sanitize_path(path: str, project_root: str = "DocuChatAPI") -> str:
    """
    Shorten file paths so they start from the project root (e.g., 'DocuChatAPI/...').
    """
    if not path:
        return path
    path = Path(path).as_posix()
    if project_root in path:
        return path[path.index(project_root) :]
    return path


def sanitize_traceback(tb: str, project_root: str = "DocuChatAPI") -> str:
    """
    Shorten all file paths inside a traceback string.
    """
    if not tb:
        return tb
    return "\n".join(sanitize_path(line, project_root) for line in tb.splitlines())


class JsonFileHandler(logging.Handler):
    """
    Logging handler that writes logs as a JSON list in a file.
    Ensures files exist and maintains logs under {"logs": [...]}.
    """

    def __init__(self, filename: Path):
        super().__init__()
        self.filename = filename
        self.filename.parent.mkdir(parents=True, exist_ok=True)
        if not self.filename.exists():
            self._write_logs([])

    def emit(self, record: logging.LogRecord):
        log_entry = record.msg
        if isinstance(log_entry, (DatabaseStandardLog, DatabaseErrorLog)):
            logs = self._read_logs()
            logs.append(log_entry.model_dump())
            self._write_logs(logs)

    def _read_logs(self) -> list:
        try:
            with self.filename.open("r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("logs", [])
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _write_logs(self, logs: list) -> None:
        with self.filename.open("w", encoding="utf-8") as f:
            json.dump({"logs": logs}, f, indent=4, default=str)


class DatabaseLogger:
    """
    Database logger that logs messages into standard-logs.json and error-logs.json.
    """

    def __init__(self, source_file: str = __name__):
        log_dir = Path(settings.database.DB_LOG_DIR)
        log_dir.mkdir(parents=True, exist_ok=True)

        self.standard_handler = JsonFileHandler(log_dir / "standard-logs.json")
        self.error_handler = JsonFileHandler(log_dir / "error-logs.json")

        self.source_file = source_file
        self.logger = logging.getLogger(source_file)
        self.logger.setLevel(logging.DEBUG)

    def _log(self, log_entry, is_error: bool = False):
        """Internal helper to send log to the right file handler."""
        handler = self.error_handler if is_error else self.standard_handler
        record = logging.LogRecord(
            name=self.logger.name,
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg=log_entry,
            args=(),
            exc_info=None,
        )
        handler.emit(record)

    def debug(
        self,
        message: str,
        action: Optional[str] = None,
        additional: Optional[dict] = None,
    ):
        """Log a debug message (used for detailed development information)."""
        log_entry = DatabaseStandardLog(
            message=message,
            level=LogLevel.DEBUG,
            action=action,
            additional=additional,
            source_file=sanitize_path(self.source_file) if self.source_file else None,
        )
        self._log(log_entry, is_error=False)

    def info(
        self,
        message: str,
        action: Optional[str] = None,
        additional: Optional[dict] = None,
    ):
        """Log an informational message (used for normal operations)."""
        log_entry = DatabaseStandardLog(
            message=message,
            level=LogLevel.INFO,
            action=action,
            additional=additional,
            source_file=sanitize_path(self.source_file) if self.source_file else None,
        )
        self._log(log_entry, is_error=False)

    def warning(
        self,
        message: str,
        action: Optional[str] = None,
        additional: Optional[dict] = None,
    ):
        """Log a warning (used for unexpected situations that are not errors)."""
        log_entry = DatabaseErrorLog(
            message=message,
            level=LogLevel.WARNING,
            action=action,
            additional=additional,
            source_file=sanitize_path(self.source_file) if self.source_file else None,
        )
        self._log(log_entry, is_error=True)

    def error(
        self,
        message: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None,
        action: Optional[str] = None,
        additional: Optional[dict] = None,
    ):
        """Log an error (used when an operation fails)."""
        log_entry = DatabaseErrorLog(
            message=message,
            level=LogLevel.ERROR,
            source_file=sanitize_path(self.source_file) if self.source_file else None,
            exception=type(exception).__name__ if exception else None,
            traceback=sanitize_traceback(traceback),
            action=action,
            additional=additional,
        )
        self._log(log_entry, is_error=True)

    def critical(
        self,
        message: str,
        exception: Optional[Exception] = None,
        traceback: Optional[str] = None,
        action: Optional[str] = None,
        additional: Optional[dict] = None,
    ):
        """Log a critical error (used for severe issues that may crash the program)."""
        log_entry = DatabaseErrorLog(
            message=message,
            level=LogLevel.CRITICAL,
            source_file=sanitize_path(self.source_file) if self.source_file else None,
            exception=type(exception).__name__ if exception else None,
            traceback=sanitize_traceback(traceback),
            action=action,
            additional=additional,
        )
        self._log(log_entry, is_error=True)
