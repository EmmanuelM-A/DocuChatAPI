"""
Defines the abstract base class for database connections.
This provides a contract for implementing different database backends
(e.g., PostgresSQL, MySQL, SQLite).
"""

from abc import ABC, abstractmethod


class AbstractDatabaseConnection(ABC):
    """
    Abstract class that defines the interface for database connections.

    This class should be used in the **infrastructure layer** of your application.
    Any concrete implementation (Postgres, MySQL, SQLite, etc.) must extend this
    and implement the abstract methods.

    Usage:
        - Define one subclass per database engine (e.g., PostgresConnection).
        - Use dependency injection in services/repositories to consume this class
          instead of binding directly to SQLAlchemy or asyncpg.

    This ensures that switching databases in the future requires minimal changes.
    """

    @abstractmethod
    async def connect(self):
        """Establish a database connection (e.g., create engine or pool)."""

    @abstractmethod
    async def disconnect(self):
        """Close the database connection and dispose resources."""

    @abstractmethod
    def get_session(self):
        """Return a session/connection object for interacting with the database."""
