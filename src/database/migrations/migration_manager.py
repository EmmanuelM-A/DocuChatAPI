"""
This module provides migration management using Alembic.
"""

from pathlib import Path
from typing import Optional, List

from alembic import command
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine

from src.config.settings import settings
from src.database.connection.base_connection import DatabaseConnection
from src.database.connection.db_connection import PostgresConnection
from src.database.migrations.alembic_env_template import ALEMBIC_ENV_TEMPLATE
from src.database.migrations.alembic_ini_template import ALEMBIC_INI_TEMPLATE

from src.logger.default_logger import logger
from src.utils.api_exceptions import DatabaseException


class MigrationManager:
    """
    This class provides a clean interface for managing database migrations
    while integrating with the existing connection infrastructure.
    """

    def __init__(self, connection: DatabaseConnection = None) -> None:
        """
        Initialize the migration manager.

        Args:
            connection: DatabaseConnection instance. If not provided a new db
                connection is created.
        """

        self._connection = connection or PostgresConnection()
        self._alembic_cfg: Optional[Config] = None
        self._migrations_path = settings.database.DB_MIGRATION_DIR

    def _get_alembic_config(self) -> Config:
        """
        Get or create the Alembic configuration.

        Returns:
            Config: Alembic configuration object
        """

        if self._alembic_cfg is None:
            # Create Alembic configuration
            self._alembic_cfg = Config()

            # Set script location (where migrations are stored)
            script_location = str(self._migrations_path)
            self._alembic_cfg.set_main_option("script_location", script_location)

            # Set database URL
            database_url = str(settings.database.DATABASE_URL.get_secret_value())
            if database_url.startswith("postgresql+asyncpg"):
                database_url = database_url.replace(
                    "postgresql+asyncpg", "postgresql+psycopg2"
                )
            self._alembic_cfg.set_main_option("sqlalchemy.url", database_url)

            # Configure file template
            file_template = settings.database.DB_MIGRATION_FILE_TEMPLATE
            self._alembic_cfg.set_main_option("file_template", file_template)

            # Set timezone
            self._alembic_cfg.set_main_option("timezone", "UTC")

        return self._alembic_cfg

    def initialize_alembic(self) -> None:
        """
        Initialize Alembic in the migrations' directory.

        This creates the alembic.ini file and versions directory structure.

        Raises:
            DatabaseException: If alembic initialization
        """

        try:
            if not Path(self._migrations_path).exists():
                command.init(str(self._migrations_path), "alembic")
            logger.debug("Alembic initialized in %s", self._migrations_path)
        except Exception as e:
            logger.error("Failed to initialize Alembic: %s", e)
            raise DatabaseException(
                error_code="ALEMBIC_INIT_FAILED",
                message=f"Alembic initialization failed: {e}",
            ) from e

    def create_migration(self, message: str, autogenerate: bool = True) -> str:
        """
        Create a new migration file.

        Args:
            message: Description of the migration
            autogenerate: Whether to auto-generate the migration from model changes

        Returns:
            str: The revision ID of the created migration

        Raises:
            DatabaseException: If migration creation fails
        """

        try:
            config = self._get_alembic_config()
            command.revision(config, message=message, autogenerate=autogenerate)
            logger.debug("Migration created: %s", message)
            return message
        except Exception as e:
            logger.error("Failed to create migration: %s", e)
            raise DatabaseException(  # FIXME: CREATE __REPR__ FOR ERROR RESPONSE
                error_code="MIGRATION_CREATION_FAILED",
                message=f"Migration creation failed: {e}",
            ) from e

    def upgrade(self, revision: str = "head") -> None:
        """
        Upgrade the database to a specific revision.

        Args:
            revision: Target revision (default: "head" for latest)

        Raises:
            DatabaseException: If upgrade fails
        """

        try:
            config = self._get_alembic_config()
            command.upgrade(config, revision)
            logger.debug("Database upgraded to revision: %s", revision)
        except Exception as e:
            logger.error("Failed to upgrade database: %s", e)
            raise DatabaseException(
                error_code="DB_UPDATE_FAILED", message=f"Database upgrade failed:: {e}"
            ) from e

    def downgrade(self, revision: str) -> None:
        """
        Downgrade the database to a specific revision.

        Args:
            revision: Target revision to downgrade to

        Raises:
            RuntimeError: If downgrade fails
        """
        try:
            config = self._get_alembic_config()
            command.downgrade(config, revision)
            logger.debug("Database downgraded to revision: %s", revision)
        except Exception as e:
            logger.error("Failed to downgrade database: %s", str(e))
            raise DatabaseException(
                error_code="DB_DOWNGRADE_FAILED",
                message=f"Database downgrade failed {e}",
            ) from e

    def get_current_revision(self) -> Optional[str]:
        """
        Get the current database revision.

        Returns:
            Optional[str]: Current revision ID, None if no migrations applied
        """
        try:
            config = self._get_alembic_config()
            script_dir = ScriptDirectory.from_config(config)

            database_url = str(settings.database.DATABASE_URL.get_secret_value())
            if database_url.startswith("postgresql+asyncpg"):
                database_url = database_url.replace(
                    "postgresql+asyncpg", "postgresql+psycopg2"
                )

            sync_engine = create_engine(database_url)

            with sync_engine.connect() as conn:
                context = MigrationContext.configure(conn)
                return context.get_current_revision()

        except Exception as e:
            logger.error("Failed to get current revision: %s", str(e))
            return None

    def get_migration_history(self) -> List[dict]:
        """
        Get the migration history.

        Returns:
            List[dict]: List of migration information dictionaries
        """

        try:
            config = self._get_alembic_config()
            script_dir = ScriptDirectory.from_config(config)

            history = []
            for revision in script_dir.walk_revisions():
                history.append(
                    {
                        "revision": revision.revision,
                        "message": revision.doc,
                        "branch_labels": revision.branch_labels,
                        "down_revision": revision.down_revision,
                    }
                )

            return history

        except Exception as e:
            logger.error("Failed to get migration history: %s", str(e))
            return []

    def check_pending_migrations(self) -> bool:
        """
        Check if there are pending migrations that haven't been applied.

        Returns:
            bool: True if there are pending migrations, False otherwise
        """
        try:
            config = self._get_alembic_config()
            script_dir = ScriptDirectory.from_config(config)

            with self._connection.engine.connect() as conn:
                context = MigrationContext.configure(conn)
                current_rev = context.get_current_revision()
                head_rev = script_dir.get_current_head()

                return current_rev != head_rev

        except Exception as e:
            logger.error("Failed to check pending migrations: %s", e)
            return False

    def show_current_info(self) -> dict:
        """
        Show current migration information.

        Returns:
            dict: Information about current migration status
        """

        current_rev = self.get_current_revision()
        pending = self.check_pending_migrations()

        return {
            "current_revision": current_rev,
            "has_pending_migrations": pending,
            "database_url": str(settings.database.DATABASE_URL.get_secret_value()),
            "migrations_path": str(self._migrations_path),
        }


class MigrationSetup:
    """
    Utility class for setting up the migration infrastructure.

    This class helps initialize the Alembic configuration files
    and directory structure within the existing project layout.
    """

    def __init__(self, migrations_path: Path = None):
        """
        Initialize the migration setup utility.

        Args:
            migrations_path: Path where migrations will be stored
        """
        self._migrations_path = migrations_path or Path(
            settings.database.DB_MIGRATION_DIR
        )

    def setup_migration_infrastructure(self) -> None:
        """
        Set up the complete migration infrastructure.

        Creates necessary directories and configuration files.
        """
        # Create migrations directory
        self._migrations_path.mkdir(parents=True, exist_ok=True)
        versions_path = self._migrations_path / "versions"
        versions_path.mkdir(exist_ok=True)

        # Create __init__.py files
        (self._migrations_path / "__init__.py").touch()
        (versions_path / "__init__.py").touch()

        # Create env.py
        env_file = self._migrations_path / "env.py"
        if not env_file.exists():
            with open(env_file, "w") as f:
                f.write(ALEMBIC_ENV_TEMPLATE)

        # Create alembic.ini in project root
        project_root = Path.cwd()
        alembic_ini = project_root / "alembic.ini"
        if not alembic_ini.exists():
            with open(alembic_ini, "w") as f:
                f.write(ALEMBIC_INI_TEMPLATE)

        logger.info(f"Migration infrastructure set up at {self._migrations_path}")

    @staticmethod
    def create_initial_migration() -> str:
        """
        Create the initial migration file.

        Returns:
            str: The revision ID of the initial migration
        """
        manager = MigrationManager()
        return manager.create_migration("Initial database schema", autogenerate=True)
