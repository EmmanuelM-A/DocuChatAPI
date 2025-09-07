#!/usr/bin/env python3
"""
Project Management CLI for DocuChatAPI.

Provides developer-friendly commands for database setup, migrations,
and other project utilities.
"""

import sys
import asyncio
from pathlib import Path
import argparse

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.scripts.setup_database import DatabaseSetupOrchestrator


def main():
    parser = argparse.ArgumentParser(description="DocuChatAPI Management CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Database commands
    db_parser = subparsers.add_parser("db", help="Database operations")
    db_subparsers = db_parser.add_subparsers(dest="db_command", required=True)

    db_subparsers.add_parser("init", help="Initialize database with migrations")
    db_subparsers.add_parser("migrate", help="Create a new migration")
    db_subparsers.add_parser("upgrade", help="Apply migrations")
    db_subparsers.add_parser("downgrade", help="Downgrade last migration")
    db_subparsers.add_parser("status", help="Show current revision")

    args = parser.parse_args()

    orchestrator = DatabaseSetupOrchestrator()

    async def run():
        if args.command == "db":
            if args.db_command == "init":
                await orchestrator.setup_migrations_infrastructure()
                await orchestrator.initialize_database()
                await orchestrator.create_initial_migration()
            elif args.db_command == "migrate":
                await orchestrator.create_initial_migration()
            elif args.db_command == "upgrade":
                await orchestrator.apply_migrations()
            elif args.db_command == "downgrade":
                await orchestrator._migration_manager.downgrade()
            elif args.db_command == "status":
                rev = orchestrator._migration_manager.get_current_revision()
                print(f"Current revision: {rev}")

    asyncio.run(run())


if __name__ == "__main__":
    main()
