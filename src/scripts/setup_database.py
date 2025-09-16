"""
Complete database setup script.

Usage:
    python src/scripts/setup_database.py [OPTIONS]

Options:
    --reset: Reset database (drop all tables and recreate)
    --no-seed: Skip seeding initial data
    --migrations-only: Only setup migration infrastructure
"""

import asyncio
import argparse
import sys
from pathlib import Path

from src.database.db_manager import DatabaseManager, get_database_manager
from src.database.migrations.migration_manager import MigrationManager, MigrationSetup

# from src.logger.default_logger import logger
from src.logger.default_logger import get_logger
from src.utils.helper import DatabaseUtil
from src.utils.api_exceptions import DatabaseException

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = get_logger(__name__)


class DatabaseSetupOrchestrator:
    """
    Orchestrates the complete database setup process.

    This class coordinates database initialization, migration setup,
    and data seeding in the correct order.
    """

    # TODO: DO FINAL DATABASE REVIEW AND CLEAN AND THEN COMPLETE TESTS

    def __init__(self):
        """Initialize the setup orchestrator."""
        # self._db_manager = DatabaseManager()
        self._db_manager = (
            get_database_manager()
        )  # TODO: FIGURE OUT WHY DB CONN NOT WORKING UPON SERVER RUN
        self.migration_manager = MigrationManager()
        self._migration_setup = MigrationSetup(migration_manager=self.migration_manager)

    async def setup_migrations_infrastructure(self) -> None:
        """
        Set up the migration infrastructure (directories, config files).
        """

        try:
            logger.debug("Setting up migration infrastructure...")
            self._migration_setup.setup_migration_infrastructure()
        except Exception as exc:
            logger.error("Migration setup failed: %s", exc)
            raise

    async def initialize_database(self, with_seed_data: bool = True) -> None:
        """
        Initialize the database with tables and optional seed data.

        Args:
            with_seed_data: Whether to populate with initial seed data
        """

        try:
            await self._db_manager.setup_database(with_seed_data=with_seed_data)
        except Exception as exc:
            logger.error("Database initialization failed: %s", str(exc))
            raise

    async def create_initial_migration(self) -> None:
        """
        Create the initial migration file based on current models.
        """

        try:
            logger.debug("Creating initial migration...")

            # Ensure database connection is established
            await self._db_manager.engine.initialize()

            # Create the migration
            revision_id = self._migration_setup.create_initial_migration()
            logger.info("Initial migration created with revision ID: %s", revision_id)

        except Exception as exc:
            logger.error(exc)
            raise

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
        """
        Reset the database by dropping and recreating everything.

        WARNING: This will permanently delete all data.
        """

        try:
            logger.warning("RESETTING DATABASE - ALL DATA WILL BE LOST")
            await self._db_manager.reset_database()
            logger.info("Database reset complete!")
        except Exception as exc:
            logger.error("Database reset failed: %s", exc)
            raise

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
        """
        Clean up resources and close connections.
        """

        try:
            await self._db_manager.shutdown()
            logger.info("Database cleanup completed")
        except Exception as exc:
            logger.error("Cleanup failed: %s", exc)
