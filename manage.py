"""
Project Management CLI for DocuChatAPI.

Provides developer-friendly commands for database setup, migrations,
and other project utilities.
"""

import sys
import asyncio
from pathlib import Path
import argparse

# from src.logger.default_logger import logger
from src.logger.default_logger import get_logger
from src.scripts.setup_database import DatabaseSetupOrchestrator
from src.utils.api_exceptions import DatabaseException

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="DocuChatAPI Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Database commands
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_subparsers = db_parser.add_subparsers(dest="db_command", required=True)

    # Init command
    db_subparsers.add_parser("init", help="Initialize database with migrations")

    # Migrate command with message
    migrate_parser = db_subparsers.add_parser("migrate", help="Create a new migration")
    migrate_parser.add_argument(
        "-m",
        "--message",
        required=True,
        help="Migration message describing the changes",
    )

    # Upgrade command
    upgrade_parser = db_subparsers.add_parser("upgrade", help="Apply migrations")
    upgrade_parser.add_argument(
        "revision", nargs="?", default="head", help="Target revision (default: head)"
    )

    # Downgrade command with required revision
    downgrade_parser = db_subparsers.add_parser(
        "downgrade", help="Downgrade to specific revision"
    )
    downgrade_parser.add_argument(
        "revision", help="Target revision to downgrade to (use -1 for previous)"
    )

    # Status command
    db_subparsers.add_parser("status", help="Show current migration status")

    # History command
    db_subparsers.add_parser("history", help="Show migration history")

    # Reset command with confirmation
    reset_parser = db_subparsers.add_parser(
        "reset", help="Reset database (DANGEROUS: drops all tables)"
    )
    reset_parser.add_argument(
        "--confirm", action="store_true", help="Confirm you want to reset the database"
    )

    # Health check command
    db_subparsers.add_parser("health", help="Check database health")

    # Seed command
    seed_parser = db_subparsers.add_parser(
        "seed", help="Seed database with initial data"
    )
    seed_parser.add_argument(
        "--skip-plans", action="store_true", help="Skip seeding plans"
    )
    seed_parser.add_argument(
        "--skip-users", action="store_true", help="Skip creating test users"
    )

    args = parser.parse_args()

    orchestrator = DatabaseSetupOrchestrator()

    async def run() -> int:
        exit_code = 0

        try:
            if args.command != "db":
                raise DatabaseException(
                    message="Database command not recognized!",
                    error_code="DB_CMD_NOT_FOUND",
                )

            if args.db_command == "init":
                logger.info("Starting database initialization...")
                await orchestrator.setup_migrations_infrastructure()
                await orchestrator.initialize_database()
                await orchestrator.create_initial_migration()
                logger.info("✅ Database initialization complete!")

            elif args.db_command == "migrate":
                logger.info("Creating new migration: %s", args.message)
                revision_id = await orchestrator.migration_manager.create_migration(
                    args.message
                )
                logger.info("✅ Migration created with revision ID: %s", revision_id)

            elif args.db_command == "upgrade":
                logger.info("Upgrading database to revision: %s", args.revision)
                await orchestrator.migration_manager.upgrade(args.revision)
                logger.info("✅ Database upgrade completed!")

            elif args.db_command == "downgrade":
                logger.warning("⚠️  Downgrading database to revision: %s", args.revision)
                await orchestrator.migration_manager.downgrade(args.revision)
                logger.info("✅ Database downgrade completed!")

            elif args.db_command == "status":
                await orchestrator.show_status()

            elif args.db_command == "history":
                history = orchestrator.migration_manager.get_migration_history()
                if not history:
                    logger.warning("No database migrations found!")
                    return exit_code

                current_rev = orchestrator.migration_manager.get_current_revision()
                logger.info("Migration History:")
                logger.info("-" * 50)

                for migration in history:
                    status_mark = "✓" if migration["revision"] == current_rev else " "
                    rev_short = (
                        migration["revision"][:8]
                        if migration["revision"]
                        else "unknown"
                    )
                    logger.info(
                        "%s %s: %s", status_mark, rev_short, migration["message"]
                    )

            elif args.db_command == "health":
                logger.info("Performing database health check...")
                health_info = await orchestrator.database_manager.engine.health_check()

                logger.info("Health Check Results:")
                logger.info("-" * 30)
                logger.info(
                    "Overall Health: %s",
                    "✅ Healthy" if health_info["healthy"] else "❌ Unhealthy",
                )

                for check_name, status in health_info["checks"].items():
                    status_icon = "✅" if status else "❌"
                    logger.info(
                        "%s %s: %s",
                        status_icon,
                        check_name.replace("_", " ").title(),
                        status,
                    )

                if health_info["metrics"]:
                    logger.info("\nMetrics:")
                    for metric, value in health_info["metrics"].items():
                        logger.info("  %s: %s", metric.replace("_", " ").title(), value)

                if health_info["errors"]:
                    logger.error("\nErrors:")
                    for error in health_info["errors"]:
                        logger.error("  - %s", error)

            elif args.db_command == "seed":
                logger.info("Seeding database with initial data...")
                seeder = orchestrator.database_manager.seeder

                if not args.skip_plans:
                    logger.info("Seeding subscription plans...")
                    await seeder.seed_plans()

                if not args.skip_users:
                    logger.info("Creating test user...")
                    await seeder.create_test_user()

                logger.info("✅ Database seeding completed!")

            elif args.db_command == "reset":
                if not args.confirm:
                    raise DatabaseException(
                        message="No database reset confirmation provided",
                        error_code="NO_DB_RESET_CONFIRMATION",
                        details="Use: python manage.py db reset --confirm",
                    )

                logger.warning("⚠️  DANGEROUS OPERATION: This will delete ALL data!")
                user_input = input("Type 'DELETE-ALL-DATA' to confirm: ")
                if user_input == "DELETE-ALL-DATA":
                    logger.warning("🗑️  Resetting database...")
                    await orchestrator.reset_database()
                    logger.info("✅ Database reset completed!")
                else:
                    logger.info("❌ Reset cancelled.")

        except DatabaseException as exc:
            logger.error("Database operation failed: %s", exc.message)
            if exc.error_detail.details:
                logger.error("Details: %s", exc.error_detail.details)
            if exc.error_detail.stack_trace:
                logger.debug("Stack trace: %s", exc.error_detail.stack_trace)
            exit_code = 1
        except IOError as exc:
            logger.error("IO Error: %s", exc)
            exit_code = 1
        except KeyboardInterrupt:
            logger.warning("Operation cancelled by user")
            exit_code = 0
        except Exception as ex:
            logger.error("Unexpected error: %s", ex, exc_info=True)
            exit_code = 1
        finally:
            await orchestrator.cleanup()

        return exit_code

    try:
        ex_code = asyncio.run(run())
        sys.exit(ex_code)
    except KeyboardInterrupt:
        logger.warning("Operation cancelled by user")
        sys.exit(0)
    except Exception as e:
        logger.error("Fatal error: %s", e, exc_info=True)
        sys.exit(1)


def show_usage_examples():
    """Display usage examples for the CLI."""
    examples = [
        ("Initialize database", "python manage.py db init"),
        ("Create migration", "python manage.py db migrate -m 'Add user table'"),
        ("Apply all migrations", "python manage.py db upgrade"),
        ("Apply to specific revision", "python manage.py db upgrade abc123"),
        ("Downgrade to previous", "python manage.py db downgrade -1"),
        ("Downgrade to specific", "python manage.py db downgrade def456"),
        ("Show current status", "python manage.py db status"),
        ("Show migration history", "python manage.py db history"),
        ("Check database health", "python manage.py db health"),
        ("Seed with initial data", "python manage.py db seed"),
        ("Reset database", "python manage.py db reset --confirm"),
    ]

    logger.info("Usage Examples:")
    logger.info("=" * 50)
    for description, command in examples:
        logger.info("  %-25s %s", description + ":", command)


if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]):
        main()
        logger.info("")
        show_usage_examples()
    else:
        main()
