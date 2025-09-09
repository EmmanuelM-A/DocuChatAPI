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

from sqlalchemy import text

from src.config.settings import settings
from src.database.db_manager import DatabaseManager
from src.database.migrations.migration_manager import MigrationManager, MigrationSetup
from src.logger.default_logger import logger
from src.utils.helper import GeneralUtil

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# TODO: Consider adding a manage.py style CLI wrapper (so instead of python
#   scripts/setup_database.py you can just run python manage.py migrate,
#   python manage.py resetdb)? This would make your project look even more
#   polished on a CV.


class DatabaseSetupOrchestrator:
    """
    Orchestrates the complete database setup process.

    This class coordinates database initialization, migration setup,
    and data seeding in the correct order.
    """

    def __init__(self):
        """Initialize the setup orchestrator."""
        self._db_manager = DatabaseManager()
        self.migration_manager = MigrationManager()
        self._migration_setup = MigrationSetup(migration_manager=self.migration_manager)

    async def setup_migrations_infrastructure(self) -> None:
        """
        Set up the migration infrastructure (directories, config files).
        """

        try:
            logger.info("Setting up migration infrastructure...")
            self._migration_setup.setup_migration_infrastructure()
            logger.info("Migration infrastructure setup complete!")
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
            logger.info("Initializing database...")
            await self._db_manager.setup_database(with_seed_data=with_seed_data)
            logger.info("Database initialization complete!")
        except Exception as exc:
            logger.error("Database initialization failed: %s", str(exc))
            raise

    async def create_initial_migration(self) -> None:
        """
        Create the initial migration file based on current models.
        """

        try:
            logger.info("Creating initial migration...")

            # Ensure database connection is established
            await self._db_manager.engine.initialize()

            # Create the migration
            revision_id = self._migration_setup.create_initial_migration()
            logger.info("Initial migration created with revision ID: %s", revision_id)

        except Exception as exc:
            logger.error("Initial migration creation failed: %s", exc)
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

    @staticmethod
    def __display_performance_metrics(health_info):
        """Display performance metrics"""

        if health_info["metrics"]:
            logger.info("\nDatabase Metrics:")
            metrics = health_info["metrics"]

            # Query response time
            if "query_response_time" in metrics:
                response_time = metrics["query_response_time"]
                logger.info("  Query Response Time: %.3f seconds", response_time)

            # Database size
            if "database_size" in metrics:
                logger.info("  Database Size: %s", metrics["database_size"])

            # Active connections
            if "active_connections" in metrics:
                logger.info("  Active Connections: %d", metrics["active_connections"])

            # Existing tables
            if "existing_tables" in metrics:
                tables = metrics["existing_tables"]
                logger.info("  Tables Found: %s", tables if tables else "None")

            # Current revision from health check
            if "current_revision" in metrics:
                current_rev = metrics["current_revision"]
                logger.info("  Current Migration: %s", current_rev or "None")
        else:
            logger.warning("No performance metrics available")

    def __display_migration_info(self, health_info):
        """Display migration information"""

        logger.info("\n=== Migration Status ===")

        # Use health check data if available, fallback to migration manager
        if "current_revision" in health_info.get("metrics", {}):
            current_rev = health_info["metrics"]["current_revision"]
            has_pending = health_info["metrics"].get("pending_migrations", False)
        else:
            # Fallback to original method
            migration_info = self.migration_manager.show_current_info()
            current_rev = migration_info["current_revision"]
            has_pending = migration_info["has_pending_migrations"]

        logger.info(
            "Current Revision: %s", current_rev or "None (no migrations applied)"
        )
        logger.info("Pending Migrations: %s", "Yes" if has_pending else "No")

        # Migration history
        history = self.migration_manager.get_migration_history()
        if history:
            logger.info("Recent Migrations:")
            for migration in history[:5]:  # Show last 5
                status = "✓" if migration["revision"] == current_rev else " "
                rev_display = (
                    migration["revision"][:8] if migration["revision"] else "unknown"
                )
                logger.info("  %s %s: %s", status, rev_display, migration["message"])
        else:
            logger.info("No migrations found")

        # Migration configuration
        migration_info = self.migration_manager.show_current_info()
        logger.info("Migrations Path: %s", migration_info["migrations_path"])

        # Summary
        logger.info("\n=== Summary ===")
        if health_info["healthy"]:
            logger.info("Database is operational and ready")
        else:
            logger.warning("⚠Database has issues that need attention")
            logger.info("   Review the errors above and run appropriate fixes")

        # Helpful commands
        if has_pending or not health_info["healthy"]:
            logger.info("\n=== Suggested Actions ===")
            if has_pending:
                logger.info("  • Apply pending migrations: python manage.py db upgrade")
            if not health_info.get("checks", {}).get("core_tables", True):
                logger.info("  • Initialize database: python manage.py db init")
            if health_info["errors"]:
                logger.info("  • Check database connection and configuration")

    async def show_status(
        self,
    ) -> None:
        """Display comprehensive database and migration status."""

        try:
            logger.info("=== Database Health Check ===")

            # Get comprehensive health information
            health_info = await self._db_manager.engine.health_check()

            # Overall health status
            health_status = "HEALTHY" if health_info["healthy"] else "UNHEALTHY"
            logger.info("Overall Status: %s", health_status)

            # Show individual check results
            if health_info["checks"]:
                logger.info("\nHealth Checks:")
                for check_name, status in health_info["checks"].items():
                    status_icon = "✓" if status else "✗"
                    check_display = check_name.replace("_", " ").title()
                    logger.info("  %s %s", status_icon, check_display)

            self.__display_performance_metrics(health_info)

            # Show any errors encountered
            if health_info["errors"]:
                logger.warning("\nHealth Check Warnings/Errors:")
                for error in health_info["errors"]:
                    logger.warning("  ⚠ %s", error)

            # Connection info (with password masking)
            logger.info("\n=== Connection Information ===")
            db_url = str(settings.database.DATABASE_URL.get_secret_value())
            masked_url = GeneralUtil.mask_db_url(db_url)

            logger.info("Database URL: %s", masked_url)
            logger.info("Pool Size: %d", settings.database.DB_POOL_SIZE)
            logger.info("Max Overflow: %d", settings.database.DB_MAX_OVERFLOW)

            self.__display_migration_info(health_info)

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
            logger.info("Cleanup complete")
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
