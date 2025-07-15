"""
Handles connections to the database and session management.
"""
from typing import Generator

from sqlmodel import SQLModel, create_engine, Session

DEFAULT_DATABASE_URL = ""


class DatabaseConnection:
    """
    Manages database engine and session lifecycle using SQLModel.

    Attributes:
        engine (Engine): SQLModel-compatible SQLAlchemy engine instance.
    """

    def __init__(
            self,
            database_url: str = DEFAULT_DATABASE_URL,
            echo: bool = True
    ):
        """
        Initializes the database engine.

        Args:
            database_url (str): The database connection string.
            echo (bool): If True, SQL statements will be logged.
        """
        self.engine = create_engine(database_url, echo=echo)

    def get_session(self) -> Generator[Session, None, None]:
        """
        Provides a generator-based database session for dependency injection
        in FastAPI.

        Yields:
            Session: A SQLModel session bound to the engine.
        """
        with Session(self.engine) as session:
            yield session

    def create_db_and_tables(self) -> None:
        """
        Creates all tables defined in SQLModel metadata.
        Useful to run at app startup.
        """
        SQLModel.metadata.create_all(self.engine)
