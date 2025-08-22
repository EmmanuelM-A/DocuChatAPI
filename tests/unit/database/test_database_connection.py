"""
Handles database connection testing.
"""

import asyncpg
import pytest

from src.config.settings import settings
from src.logger.default_logger import logger

DATABASE_URL = str(settings.database.DATABASE_URL.get_secret_value())


class TestDatabaseConnection:
    """Tests if the application can connect to the database"""

    @pytest.mark.asyncio
    async def test_database_connection(self):
        """Tests if the database connection can be successfully made."""

        conn = None
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            result = await conn.fetchval("SELECT version()")

            logger.info(f"Connection successful! PostgresSQL version: {result}")
            assert result is not None, "Expected PostgresSQL version but got None"

        finally:
            if conn is not None:
                await conn.close()

    @pytest.mark.asyncio
    async def test_table_creation(self):
        """Tests if table creation is possible in the database."""

        conn = None
        try:
            conn = await asyncpg.connect(DATABASE_URL)
            result = await conn.execute(
                """
                CREATE TABLE IF NOT EXISTS test_table (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(50)
                )
                """
            )

            logger.info("Table creation successful!")
            assert result.startswith("CREATE TABLE") or result.startswith("CREATE TABLE IF NOT EXISTS")

        finally:
            if conn is not None:
                await conn.close()
