"""
Concrete implementation of AbstractDatabaseConnection for PostgresSQL
using SQLAlchemy with asyncpg. Handling connections to the database and session
management.
"""

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from src.database.connection.base_connection import AbstractDatabaseConnection
from src.config.settings import settings
from utils.api_exceptions import DatabaseException


class PostgresConnection(AbstractDatabaseConnection):
    """
    PostgresSQL database connection implementation using SQLAlchemy async engine.

    This class handles connection pooling, session management, and cleanup.
    """

    def __init__(self, database_url: str = None):
        self.database_url = database_url or str(
            settings.database.DATABASE_URL.get_secret_value()
        )
        self.engine = None
        self.session_maker = None

    async def connect(self):
        """Create the async SQLAlchemy engine and session factory."""
        self.engine = create_async_engine(
            url=self.database_url,
            echo=settings.database.DB_ECHO,
            pool_pre_ping=settings.database.DB_IS_POOL_PRE_PING_ENABLED,
            pool_size=settings.database.DB_POOL_SIZE,
            max_overflow=settings.database.DB_MAX_OVERFLOW,
        )
        self.session_maker = async_sessionmaker(
            bind=self.engine, expire_on_commit=False, autoflush=False
        )

    async def disconnect(self):
        """Dispose the engine and close connections."""
        if self.engine:
            await self.engine.dispose()

    def get_session(self) -> AsyncSession:
        """
        Get a new database session.

        Returns:
            AsyncSession: A SQLAlchemy asynchronous session object.
        """
        if not self.session_maker:
            raise DatabaseException(
                error_code="NO_DB_CONNECTION_DETECTED",
                message="Database not connected. Call connect() first.",
            )
        return self.session_maker()
