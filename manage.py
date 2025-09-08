#!/usr/bin/env python3
"""
Project Management CLI for DocuChatAPI.

Provides developer-friendly commands for database setup, migrations,
and other project utilities.
"""

# TODO: USE LOGGING INSTEAD OF PRINTS

import sys
import asyncio
from pathlib import Path
import argparse

from src.scripts.setup_database import DatabaseSetupOrchestrator

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))


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

    args = parser.parse_args()

    orchestrator = DatabaseSetupOrchestrator()

    async def run():
        try:
            if args.command == "db":
                if args.db_command == "init":
                    print("Initializing database and migration infrastructure...")
                    await orchestrator.setup_migrations_infrastructure()
                    await orchestrator.initialize_database()
                    await orchestrator.create_initial_migration()
                    print("Database initialization complete!")

                elif args.db_command == "migrate":
                    print(f"Creating new migration: {args.message}")
                    await orchestrator.migration_manager.create_migration(args.message)
                    print("Migration created successfully!")

                elif args.db_command == "upgrade":
                    print(f"Upgrading database to: {args.revision}")
                    await orchestrator.migration_manager.upgrade(args.revision)
                    print("Database upgrade complete!")

                elif args.db_command == "downgrade":
                    print(f"Downgrading database to: {args.revision}")
                    await orchestrator.migration_manager.downgrade(args.revision)
                    print("Database downgrade complete!")

                elif args.db_command == "status":
                    print("Current database status:")
                    await orchestrator.show_status()

                elif args.db_command == "history":
                    print("Migration history:")
                    history = orchestrator.migration_manager.get_migration_history()
                    if not history:
                        print("No migrations found.")
                    else:
                        current_rev = (
                            orchestrator.migration_manager.get_current_revision()
                        )
                        for migration in history:
                            status_mark = (
                                "✓" if migration["revision"] == current_rev else " "
                            )
                            rev_short = (
                                migration["revision"][:8]
                                if migration["revision"]
                                else "unknown"
                            )
                            print(
                                f"  {status_mark} {rev_short}: {migration['message']}"
                            )

                elif args.db_command == "reset":
                    if not args.confirm:
                        print("ERROR: Database reset requires confirmation.")
                        print("This will permanently delete ALL data in the database.")
                        print("Use: python manage.py db reset --confirm")
                        return

                    print("WARNING: This will permanently delete ALL data!")
                    user_input = input("Type 'DELETE ALL DATA' to confirm: ")
                    if user_input == "DELETE ALL DATA":
                        print("Resetting database...")
                        await orchestrator.reset_database()
                        print("Database reset complete!")
                    else:
                        print("Reset cancelled.")

        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
        finally:
            await orchestrator.cleanup()

    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Fatal error: {e}")
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
        ("Reset database", "python manage.py db reset --confirm"),
    ]

    print("Usage Examples:")
    for description, command in examples:
        print(f"  {description:<25} {command}")


if __name__ == "__main__":
    if len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] in ["-h", "--help"]):
        main()
        print("\n" + "=" * 50)
        show_usage_examples()
    else:
        main()
