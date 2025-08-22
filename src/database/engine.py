"""
Responsible for database engine and Setup.
"""

from typing import Optional, AsyncGenerator
from contextlib import asynccontextmanager
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from logger.default_logger import logger
from src.database.connection.db_connection import PostgresConnection
from src.database.models.base import Base
from src.config.settings import settings
from utils.api_exceptions import DatabaseException


class DatabaseEngine:
    """
    Handles database initialization, health checks, and session management.
    """

    def __init__(self, connection: PostgresConnection = None):
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
            raise DatabaseException(
                error_code="DB_INIT_FAILED",
                message=f"Database initialization failed: {e}",
            )

    async def shutdown(self) -> None:
        """
        Shutdown the database connection and cleanup resources.
        """
        try:
            await self._connection.disconnect()
            self._is_initialized = False
            logger.info("Database engine shutdown completed")
        except Exception as e:
            logger.error(f"Error during database shutdown: {e}")
            raise

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
                error_code="DB_ENGINE_NOT_INIT",
                message="Database engine has not been initialized",
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
            await self.initialize()

        try:
            async with self._connection.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
        except SQLAlchemyError as e:
            logger.error(f"Failed to create database tables: {e}")
            raise RuntimeError(f"Table creation failed: {e}")

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
            logger.error(f"Failed to drop database tables: {e}")
            raise RuntimeError(f"Table dropping failed: {e}")

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
            logger.error(f"Database health check failed: {e}")
            return False
