"""
Handles database connection testing.
"""

from src.config.settings import settings
import asyncpg

from src.logger.default_logger import get_logger

logger = get_logger("TEST_DB_CONN")

DATABASE_URL = str(settings.database.DATABASE_URL.get_secret_value())


class TestDatabaseConnection:
    """Tests if the application can connect to the database"""

    async def test_database_connection(self):
        """Tests if the database connection can be successfully made."""

        conn = None
        try:
            # Test basic connection
            conn = await asyncpg.connect(DATABASE_URL)

            # Test query
            result = await conn.fetchval("SELECT version()")

            logger.info(f"Connection successful! PostgresSQL version: {result}")

        except Exception as e:
            logger.error(f"Connection failed: {e}")
        finally:
            if conn is not None:
                await conn.close()

    async def test_table_creation(self):
        """Tests if table creation is possible in the database."""

        conn = None
        try:
            # Test basic connection
            conn = await asyncpg.connect(DATABASE_URL)

            # Test table creation
            await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50)
                )
                """
            )

            logger.info("Table creation successful!")

        except Exception as e:
            logger.error(f"Connection failed: {e}")
        finally:
            if conn is not None:
                await conn.close()
