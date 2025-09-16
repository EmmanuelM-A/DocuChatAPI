from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database.db_manager import get_database_manager
from src.logger.default_logger import logger
from src.database.database_utils import DatabaseUtil

# TODO: FIX MIGRATION AND DB CONNECTION ISSUES


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown tasks.

    Startup responsibilities:
    - Initialize database connection
    - Verify database health
    - Check migration status
    - Validate required tables exist

    Does NOT:
    - Create tables (use migrations)
    - Run migrations (use manage.py)
    - Seed data (use manage.py)
    """

    db_manager = get_database_manager()

    try:
        logger.info("Starting DocuChatAPI application...")

        # Initialize connection only
        await db_manager.initialize_for_application()

        # Retrieve health check info
        health_info = await db_manager.engine.health_check()

        # Verify database health
        DatabaseUtil.is_database_healthy(health_info)

        # Check that the required tables exist
        DatabaseUtil.verify_tables_exist(health_info)

        # Check pending migrations (don't run)
        DatabaseUtil.check_migration_status(health_info)

        yield
    except Exception as e:
        raise e
    finally:
        logger.debug("Shutting down application...")
        try:
            await db_manager.shutdown()
        except Exception as e:
            logger.error("Error during shutdown: %s", str(e))
