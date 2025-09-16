"""
Stores utility functions and classes for database operations.
"""

from typing import Any

from src.logger.default_logger import get_logger
from src.config.settings import settings

# from src.logger.default_logger import logger

logger = get_logger(__name__)


class DatabaseUtil:
    """Application wide utility functions for the database and its operations."""

    @staticmethod
    def mask_db_url(db_url) -> str:
        """Censures the sensitive information found in a database url."""

        try:
            if "://" in db_url:
                protocol, rest = db_url.split("://", 1)
                if "@" in rest:
                    credentials, host_part = rest.split("@", 1)

                    if ":" in credentials:
                        username = credentials.split(":")[0]
                        return f"{protocol}://{username}:***@{host_part}"

                    return f"{protocol}://***@{host_part}"
                else:
                    return db_url  # No credentials in URL
            else:
                return "***"  # Fallback for unexpected format
        except Exception:
            return "*** (URL format not recognized)"

    @staticmethod
    def is_database_healthy(health_info: dict[str, Any]):
        """Determines if the database is healthy or not"""

        logger.info(f"{"=" * 20} DATABASE HEALTH STATUS {"=" * 20}")

        health_status = "HEALTHY" if health_info["healthy"] else "UNHEALTHY"

        if health_info["healthy"]:
            logger.info(f"Database status: {health_status}")
        else:
            logger.warning(f"Database status: {health_status}")

    @staticmethod
    def log_health_checks(health_info: dict[str, Any]):
        """Displays all health checks"""

        logger.info(f"{"=" * 20} DATABASE HEALTH CHECK {"=" * 20}")

        if health_info.get("checks"):
            for check_name, status in health_info["checks"].items():
                check_display = check_name.replace("_", " ").title()
                if status:
                    logger.info(f"Health check passed: {check_display}")
                else:
                    logger.warning(f"Health check failed: {check_display}")
        else:
            logger.warning("No health checks available")

    @staticmethod
    def log_performance_metrics(health_info: dict[str, Any]):
        """Logs database performance metrics"""

        logger.info(f"{"=" * 20} DATABASE PERFORMANCE METRICS {"=" * 20}")

        metrics = health_info.get("metrics", {})

        if metrics:
            if "query_response_time" in metrics:
                response_time = metrics["query_response_time"]
                logger.info(f"Query response time: {response_time:.3f}s")

            if "database_size" in metrics:
                logger.info(f"Database size: {metrics['database_size']}")

            if "active_connections" in metrics:
                logger.info(f"Active connections: {metrics['active_connections']}")

            if "existing_tables" in metrics:
                table_count = len(metrics["existing_tables"])
                logger.info(f"Tables found: {table_count}")
        else:
            logger.warning("No performance metrics available")

    @staticmethod
    def log_errors_encountered(health_info: dict[str, Any]):
        """Log any errors encountered during health checks"""

        logger.info(f"{"=" * 20} DATABASE ERRORS {"=" * 20}")

        errors = health_info.get("errors", [])

        if errors:
            for error in errors:
                logger.error(f"Health check error: {error}")
        else:
            logger.info("No errors encountered during health check")

    @staticmethod
    def log_connection_data():
        """Log database connection information (with sensitive data masked)"""

        logger.info(f"{"=" * 20} DATABASE CONNECTION INFO {"=" * 20}")

        db_url = str(settings.database.DATABASE_URL.get_secret_value())
        masked_url = DatabaseUtil.mask_db_url(db_url)

        logger.info(f"Database URL: {masked_url}")
        logger.info(f"Pool size: {settings.database.DB_POOL_SIZE}")
        logger.info(f"Max overflow: {settings.database.DB_MAX_OVERFLOW}")

    @staticmethod
    def check_migration_status(health_info: dict[str, Any]):
        """Check and log migration status"""

        logger.info(f"{"=" * 20} DATABASE MIGRATION CHECK {"=" * 20}")

        metrics = health_info.get("metrics", {})
        current_revision = metrics.get("current_revision")
        has_pending = metrics.get("pending_migrations", False)

        if current_revision:
            logger.info(f"Current migration revision: {current_revision[:8]}")
        else:
            logger.info("No migrations applied")

        if has_pending:
            logger.warning("Pending migrations detected")

    @staticmethod
    def log_migration_info(health_info: dict[str, Any]):
        """Log detailed migration information"""

        logger.info(f"{"=" * 20} DATABASE MIGRATION INFO {"=" * 20}")

        metrics = health_info.get("metrics", {})
        current_revision = metrics.get("current_revision")

        if current_revision:
            logger.info(f"Migration status: {current_revision[:8]} applied")
        else:
            logger.info("Migration status: No migrations applied")

    @staticmethod
    def verify_tables_exist(health_info: dict[str, Any]):
        """Verify that required tables exist in the database"""

        logger.info(f"{"=" * 20} DATABASE TABLES CHECK {"=" * 20}")

        metrics = health_info.get("metrics", {})
        existing_tables = metrics.get("existing_tables", [])

        if existing_tables:
            logger.info(
                f"Database tables verified: {len(existing_tables)} tables found"
            )
        else:
            logger.warning("No tables found in database")
