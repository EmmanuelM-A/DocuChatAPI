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
from src.logger.default_logger import logger
from src.utils.helper import DatabaseUtil
from src.utils.api_exceptions import DatabaseException

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


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


async def main():
    """
    Main setup function with command-line argument handling.
    """
    parser = argparse.ArgumentParser(description="Database Setup for DocuChatAPI")
    parser.add_argument(
        "--reset", action="store_true", help="Reset database (DROPS ALL TABLES)"
    )
    parser.add_argument(
        "--no-seed", action="store_true", help="Skip seeding initial data"
    )
    parser.add_argument(
        "--migrations-only",
        action="store_true",
        help="Only setup migration infrastructure",
    )
    parser.add_argument(
        "--status", action="store_true", help="Show current database status"
    )
    parser.add_argument(
        "--apply-migrations", action="store_true", help="Apply pending migrations only"
    )

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = DatabaseSetupOrchestrator()

    try:
        if args.status:
            # Show status only
            await orchestrator.show_status()
            return

        if args.apply_migrations:
            # Apply migrations only
            await orchestrator.apply_migrations()
            await orchestrator.show_status()
            return

        if args.migrations_only:
            # Setup migration infrastructure only
            await orchestrator.setup_migrations_infrastructure()
            await orchestrator.create_initial_migration()
            logger.info("   Migration infrastructure setup complete!")
            logger.info("   Next steps:")
            logger.info("   1. Review the generated migration file")
            logger.info(
                "   2. Run: python scripts/setup_database.py --apply-migrations"
            )
            return

        # Full setup process
        logger.info("Starting DocuChatAPI database setup...")

        # Setup migration infrastructure
        await orchestrator.setup_migrations_infrastructure()

        if args.reset:
            # Reset database if requested
            await orchestrator.reset_database()
        else:
            # Normal initialization
            seed_data = not args.no_seed
            await orchestrator.initialize_database(with_seed_data=seed_data)

        # Create initial migration if it doesn't exist
        try:
            await orchestrator.create_initial_migration()
        except Exception as exc:
            # Initial migration might already exist, that's okay
            logger.info("️  Initial migration handling: %s", exc)

        # Apply any pending migrations
        await orchestrator.apply_migrations()

        # Show final status
        await orchestrator.show_status()

        logger.info("Database setup completed successfully!")

        if not args.no_seed:
            logger.info("Default data created:")
            logger.info("   Subscription plans: free")
            logger.info("   Test user: test@example.com (password: P@ssword123)")

        logger.info("Available commands:")
        logger.info("   python scripts/setup_database.py --status")
        logger.info("   python scripts/setup_database.py --apply-migrations")
        logger.info("   python scripts/setup_database.py --reset")

    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
    except Exception as exc:
        logger.error("Setup failed with error: %s", exc)
        import traceback

        traceback.print_exc()
        sys.exit(1)
    finally:
        await orchestrator.cleanup()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n  Setup interrupted")
        sys.exit(0)
    except Exception as e:
        print(f"\n  Fatal error: {e}")
        sys.exit(1)
