"""
This module provides the database engine management and initialization.
"""

from decimal import Decimal
from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager

import bcrypt
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from src.database.connection.base_connection import DatabaseConnection
from src.database.models.plan_model import Plan
from src.database.models.user_model import User
from src.logger.default_logger import logger
from src.database.connection.db_connection import PostgresConnection
from src.database.models.base_model import Base
from src.config.settings import settings
from src.utils.api_exceptions import DatabaseException


class DatabaseEngine:
    """
    Handles database initialization, health checks, and session management.
    """

    def __init__(self, connection: DatabaseConnection = None):
        """
        Initialize the database engine.

        Args:
            connection: Optional PostgresConnection instance.
                       If not provided, creates a new one.
        """
        self._connection = connection or PostgresConnection()
        self._is_initialized = False

    @property
    def is_initialized(self) -> bool:
        """Check if the database engine is initialized."""
        return self._is_initialized

    async def initialize(self) -> None:
        """
        Initialize the database connection and engine.

        Raises:
            RuntimeError: If initialization fails.
        """
        try:
            await self._connection.connect()
            self._is_initialized = True
            logger.info("Database engine initialized successfully")
        except Exception as e:
            # Ensure cleanup on failure
            try:
                if self._connection.engine:
                    await self._connection.disconnect()
            except Exception as cleanup_error:
                logger.error("Cleanup failed during initialization: %s", cleanup_error)

            self._is_initialized = False

            raise DatabaseException(
                message="Database initialization failed.",
                error_code="DB_INIT_FAILED",
                stack_trace=str(e),
            ) from e

    async def shutdown(self) -> None:
        """
        Shutdown the database connection and cleanup resources.
        """
        try:
            await self._connection.disconnect()
            self._is_initialized = False
            logger.info("Database engine shutdown completed")
        except Exception as e:
            logger.error("Error during database shutdown: %s", e)
            raise DatabaseException(
                message="The database failed to shutdown",
                error_code="DB_SHUTDOWN_ERROR",
                stack_trace=str(e),
            ) from e
        # finally:
        #     if not self._is_initialized: # TODO: LOOK INTO THIS
        #         logger.info("Initiating second attempt at shutting down the database.")

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get a database session with automatic transaction management.

        Usage:
            async with engine.get_session() as session:
                # Use session here
                result = await session.execute(select(User))

        Yields:
            AsyncSession: SQLAlchemy async session with auto-commit/rollback

        Raises:
            RuntimeError: If database is not initialized
        """
        if not self._is_initialized:
            raise DatabaseException(
                message="Database engine has not been initialized",
                error_code="DB_ENGINE_NOT_INIT",
            )

        session = self._connection.get_session()
        try:
            async with session:
                yield session
                await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_tables(self) -> None:
        """
        Create all database tables based on SQLAlchemy models.

        Raises:
            RuntimeError: If table creation fails
        """
        if not self._is_initialized:
            logger.warning("Database has not been initialized yet. Initiating now...")
            await self.initialize()

        try:
            async with self._connection.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error("Failed to create database tables: %s", e)
            raise DatabaseException(
                message=f"Table creation failed: {e}",
                error_code="TABLE_CREATION_FAILED",
            ) from e
        except Exception as e:
            logger.error("Unexpected error creating tables: %s", e)
            raise DatabaseException(
                message=f"Unexpected table creation error: {e}",
                error_code="TABLE_CREATION_UNEXPECTED_ERROR",
            ) from e

    async def drop_tables(self) -> None:
        """
        Drop all database tables - USE WITH EXTREME CAUTION.

        This will permanently delete all data in the database.

        Raises:
            RuntimeError: If table dropping fails
        """

        if settings.database.DB_SAFETY_ENABLED:
            logger.warning(
                "Database safety enabled! If you wish to execute "
                "operation, disable it and then enable again!"
            )
            return

        if not self._is_initialized:
            await self.initialize()

        try:
            async with self._connection.engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
            logger.warning("All database tables dropped - DATA LOST")
        except SQLAlchemyError as e:
            logger.error("Failed to drop database tables: %s", e)
            raise DatabaseException(
                message=f"Table dropping failed: {e}", error_code="TABLE_DROP_FAILED"
            ) from e

    async def health_check(self) -> bool:
        """
        Perform a database health check.

        Returns:
            bool: True if database is healthy, False otherwise
        """
        try:
            async with self.get_session() as session:
                await session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error("Database health check failed: %s", e)
            return False


# TODO: CHAT WITH THE DATA: https://claude.ai/chat/9c5fcad0-959b-4306-9dc6-8321369a7637


class DatabaseSeeder:
    """
    Database seeding class for populating initial data.

    Handles creation of default plans, test users, and other seed data
    in an idempotent manner (won't create duplicates).
    """

    def __init__(self, engine: DatabaseEngine):
        """
        Initialize the database seeder.

        Args:
            engine: DatabaseEngine instance for database operations
        """
        self._engine = engine

    async def seed_plans(self) -> None:
        """
        Create default subscription plans if they don't exist.

        Creates three plans: free, pro, and enterprise with appropriate limits.
        """

        async with self._engine.get_session() as session:
            # Check if plans already exist
            result = await session.execute(text("SELECT COUNT(*) FROM plan"))
            count = result.scalar()

            if count > 0:
                logger.info("Plans already exist, skipping seed")
                return

            # Create default plans
            plans = [
                Plan(
                    name="free",
                    token_limit_daily=10000,
                    document_limit=5,
                    session_limit=1,
                    price_monthly=Decimal("0.00"),
                    is_active=True,
                )
            ]

            session.add_all(plans)
            await session.commit()
            logger.info("Default subscription plans created successfully")

    async def create_test_user(
        self,
        username: str = "TestUser",
        email: str = "test@example.com",
        password: str = "P@ssword123",
    ) -> None:
        """
        Create a test user for development purposes.

        Args:
            username: Username for the test user
            email: Email address for the test user
            password: Plain password (will be hashed)
        """

        async with self._engine.get_session() as session:
            # Get free plan ID
            result = await session.execute(
                text("SELECT id FROM plan WHERE name = 'free' LIMIT 1")
            )
            plan_id = result.scalar()

            if not plan_id:
                logger.error("Free plan not found. Run seed_plans() first.")
                raise DatabaseException(
                    error_code="NO_FREE_PLAN_FOUND", message="Free plan not found"
                )

            # Check if user already exists
            result = await session.execute(
                text('SELECT COUNT(*) FROM "user" WHERE email = :email'),
                {"email": email},
            )
            count = result.scalar()

            if count > 0:
                logger.info("Test user %s already exists", email)
                return

            # Create test user
            test_user = User(
                username=username,
                email=email,
                hashed_password=bcrypt.hashpw(
                    password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8"),
                plan_id=plan_id,
                email_verified=True,
                is_active=True,
            )

            session.add(test_user)
            await session.commit()
            logger.info("Test user created: %s (password: %s)", email, password)

    async def seed_all(self) -> None:
        """
        Run all seeding operations in the correct order.

        This method ensures plans are created before users that reference them.
        """
        try:
            await self.seed_plans()
            await self.create_test_user()
            logger.info("Database seeding completed successfully")
        except Exception as e:
            logger.error("Database seeding failed: %s", e)
            raise DatabaseException(
                message="An error occurred during database seeding",
                error_code="DB_SEEDING_FAILED",
                stack_trace=str(e),
            ) from e


class DatabaseManager:
    """
    High-level database manager that coordinates engine and seeding operations.

    This class provides a unified interface for database initialization,
    management, and maintenance operations.
    """

    def __init__(self):
        """Initialize the database manager with default components."""
        self._engine = DatabaseEngine()
        self._seeder = DatabaseSeeder(self._engine)

    @property
    def engine(self) -> DatabaseEngine:
        """Get the database engine instance."""
        return self._engine

    @property
    def seeder(self) -> DatabaseSeeder:
        """Get the database seeder instance."""
        return self._seeder

    async def setup_database(self, with_seed_data: bool = True) -> None:
        """
        Complete database setup including initialization, table creation, and seeding.

        Args:
            with_seed_data: Whether to populate the database with initial seed data

        Raises:
            RuntimeError: If setup fails at any stage
        """
        try:
            logger.info("Starting database setup...")

            # Initialize connection
            await self._engine.initialize()

            # Create tables
            await self._engine.create_tables()

            # Seed data if requested
            if with_seed_data:
                await self._seeder.seed_all()

            # Health check
            is_healthy = await self._engine.health_check()
            if not is_healthy:
                raise DatabaseException(
                    message="Database health check failed after setup",
                    error_code="DB_HEALTH_CHECK_FAILED",
                )

            logger.info("Database setup completed successfully")

        except Exception as e:
            logger.error("Database setup failed: %s", e)
            await self._engine.shutdown()
            raise DatabaseException(
                message="Database setup failed", error_code="DB_SETUP_FAILED"
            ) from e

    async def reset_database(self) -> None:
        """
        Reset the database by dropping and recreating all tables with seed data.

        WARNING: This will permanently delete all data in the database.

        Raises:
            RuntimeError: If reset operation fails
        """
        try:
            logger.warning("Starting database reset - ALL DATA WILL BE LOST")

            if not self._engine.is_initialized:
                await self._engine.initialize()

            # Drop and recreate tables
            await self._engine.drop_tables()
            await self._engine.create_tables()

            # Reseed data
            await self._seeder.seed_all()

            logger.info("Database reset completed successfully")

        except Exception as e:
            logger.error("Database reset failed: %s", e)
            raise DatabaseException(
                message="Databased failed to reset",
                error_code="DB_RESET_FAILED",
                stack_trace=str(e),
            ) from e

    async def shutdown(self) -> None:
        """Gracefully shutdown the database manager."""
        await self._engine.shutdown()


# Singleton instance for application use
_db_manager: Optional[DatabaseManager] = None


def get_database_manager() -> DatabaseManager:
    """
    Get the singleton database manager instance.

    Returns:
        DatabaseManager: The application's database manager instance
    """
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager


# Dependency for FastAPI or other frameworks
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency for getting database sessions.

    Usage in FastAPI:
        @app.get("/users")
        async def get_users(session: AsyncSession = Depends(get_db_session)):
            # Use session here

    Yields:
        AsyncSession: Database session for request handling
    """
    db_manager = get_database_manager()
    async with db_manager.engine.get_session() as session:
        yield session
