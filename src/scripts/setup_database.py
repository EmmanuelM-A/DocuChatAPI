"""
Database setup orchestrator that coordinates database initialization,
migrations, and seeding operations.
"""

import sys
from pathlib import Path

from src.database.db_manager import get_database_manager
from src.database.migrations.migration_manager import MigrationManager, MigrationSetup

# from src.logger.default_logger import logger
from src.logger.default_logger import get_logger
from src.database.database_utils import DatabaseUtil
from src.utils.api_exceptions import DatabaseException

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = get_logger(__name__)

# TODO: DO FINAL DATABASE REVIEW AND CLEAN AND THEN COMPLETE TESTS


class DatabaseSetupOrchestrator:
    """
    Orchestrates database setup operations including initialization,
    migrations, and seeding.

    This class provides a high-level interface for the manage.py CLI
    and coordinates between different database components.
    """

    def __init__(self):
        """Initialize the setup orchestrator."""

        self._db_manager = get_database_manager()
        self._migration_manager = MigrationManager()
        self._migration_setup = MigrationSetup(
            migration_manager=self._migration_manager
        )
        self._initialized = False

    @property
    def db_manager(self):
        """Returns the instance of the database manager"""
        return self._db_manager

    @property
    def migration_manager(self):
        """Returns the instance of the migration manager"""
        return self._migration_manager

    async def initialize_database(self) -> None:
        """Initialize database connection and engine."""
        try:
            await self._db_manager.initialize_for_application()
            self._initialized = True
        except Exception as e:
            raise DatabaseException(
                message="Failed to initialize database",
                error_code="DB_INIT_FAILED",
                stack_trace=str(e),
            ) from e

    async def setup_migrations_infrastructure(self) -> None:
        """Set up the migration infrastructure (directories, config files, etc.)."""
        try:
            self._migration_setup.setup_migration_infrastructure()
        except Exception as e:
            raise DatabaseException(
                message="Failed to setup migration infrastructure",
                error_code="MIGRATION_SETUP_FAILED",
                stack_trace=str(e),
            ) from e

    async def create_initial_migration(self) -> str:
        """Create the initial database migration."""
        try:
            if not self._initialized:
                await self.initialize_database()

            revision_id = self._migration_setup.create_initial_migration()

            logger.info("Initial migration created: %s", revision_id)

            return revision_id
        except Exception as e:
            raise DatabaseException(
                message="Failed to create initial migration",
                error_code="INITIAL_MIGRATION_FAILED",
                stack_trace=str(e),
            ) from e

    async def apply_migrations(self) -> None:
        """
        Apply all pending migrations to bring database to latest state.
        """

        try:
            logger.info("Applying database migrations...")

            # Check if there are pending migrations
            has_pending = self.migration_manager.check_pending_migrations()
            if has_pending:
                self.migration_manager.upgrade()
                logger.info("Migrations applied successfully!")
            else:
                logger.info("No pending migrations found!")

        except Exception as exc:
            logger.error("Migration application failed: %s", str(exc))
            raise

    async def reset_database(self) -> None:
        """Reset the entire database (drops all tables and recreates)."""
        try:
            if not self._initialized:
                await self.initialize_database()

            await self._db_manager.reset_database()
        except Exception as e:
            raise DatabaseException(
                message="Database reset failed",
                error_code="DB_RESET_FAILED",
                stack_trace=str(e),
            ) from e

    async def show_status(self) -> None:
        """Display comprehensive database and migration status."""

        try:
            # Initialize database connection
            await self._db_manager.engine.initialize()

            # Get comprehensive health information
            health_info = await self._db_manager.engine.health_check()

            # Database status
            DatabaseUtil.is_database_healthy(health_info)

            # Show individual check results
            DatabaseUtil.log_health_checks(health_info)

            DatabaseUtil.log_performance_metrics(health_info)

            DatabaseUtil.log_errors_encountered(health_info)

            # Connection info (with password masking)
            DatabaseUtil.log_connection_data()

            DatabaseUtil.check_migration_status(health_info)

            DatabaseUtil.log_migration_info(health_info)

            DatabaseUtil.verify_tables_exist(health_info)
        except DatabaseException as ex:
            logger.error(ex)
        except Exception as exc:
            logger.warning("Failed to get status: %s", str(exc))
            # Fallback to basic status if comprehensive check fails
            logger.debug("Falling back to basic status check...")
            try:
                basic_healthy = await self._db_manager.engine.health_check()
                logger.info(
                    "Basic Health Check: %s",
                    "HEALTHY" if basic_healthy else "UNHEALTHY",
                )
            except Exception as basic_exc:
                logger.error("Basic health check also failed: %s", str(basic_exc))

    async def cleanup(self) -> None:
        """Clean up resources."""

        try:
            if self._initialized:
                await self._db_manager.shutdown()
                self._initialized = False
                logger.debug("Database orchestrator cleanup completed")
        except Exception as e:
            logger.warning("Cleanup warning: %s", e)
