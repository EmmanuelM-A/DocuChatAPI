"""
Configuration settings for the DocuChatAPI application.
Each configuration class handles a specific domain of settings.
"""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# ------------------------------------------------------------------
# Load .env file explicitly
# ------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
ENV_FILE = PROJECT_ROOT / ".env"

if ENV_FILE.exists():
    load_dotenv(ENV_FILE)


# ------------------------------------------------------------------
# Core Settings
# ------------------------------------------------------------------
class CoreAppSettings(BaseSettings):
    ENV: str = Field(default="development", env="ENV")
    APP_NAME: str = Field(default="DocuChatAPI")
    DEBUG_ENABLED: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Database Settings
# ------------------------------------------------------------------
class DatabaseSettings(BaseSettings):
    DATABASE_URL: SecretStr = Field(default=..., env="DATABASE_URL")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default="docu_chat", env="DB_NAME")
    DB_USER: str = Field(default="postgres", env="DB_USER")
    DB_PASSWORD: SecretStr = Field(default="", env="DB_PASSWORD")

    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    DB_POOL_TIMEOUT: int = Field(default=30)
    DB_ECHO: bool = Field(default=True)
    DB_IS_POOL_PRE_PING_ENABLED: bool = Field(default=True)

    DB_SAFETY_ENABLED: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Authentication Settings
# ------------------------------------------------------------------
class AuthSettings(BaseSettings):
    """
    Authentication and authorization configuration settings.
    """

    # ACCESS_SECRET: SecretStr = Field(..., env="ACCESS_TOKEN_SECRET")
    # REFRESH_SECRET: SecretStr = Field(..., env="REFRESH_TOKEN_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=5)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# File Processing Settings
# ------------------------------------------------------------------
class FileProcessingSettings(BaseSettings):
    ALLOWED_FILE_EXTENSIONS: List[str] = Field(default=[".pdf", ".docx", ".txt", ".md"])
    MAX_FILE_SIZE_MB: int = Field(default=20)
    MAX_FILES_PER_UPLOAD: int = Field(default=10)

    RAW_DOCS_DIRECTORY: str = Field(default="../data/raw_docs")
    PROCESSED_DOCS_DIRECTORY: str = Field(default="../data/processed_docs")

    MD_FILE_EXT: str = Field(default=".md")
    TXT_FILE_EXT: str = Field(default=".txt")
    PDF_FILE_EXT: str = Field(default=".pdf")
    DOCX_FILE_EXT: str = Field(default=".docx")

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# LLM Integration
# ------------------------------------------------------------------
class LLMIntegrationSettings(BaseSettings):
    # OPENAI_API_KEY: SecretStr = Field(default=..., env="OPENAI_API_KEY")
    LLM_MODEL_NAME: str = Field(default="gpt-3.5-turbo")
    EMBEDDING_MODEL_NAME: str = Field(default="text-embedding-3-small")

    LLM_TEMPERATURE: float = Field(default=0.7)
    MAX_TOKENS: int = Field(default=4096)

    OPENAI_API_RATE_LIMIT: int = Field(default=60)
    OPENAI_API_TIMEOUT_SEC: int = Field(default=30)
    MAX_API_RETRIES: int = Field(default=3)
    API_RETRY_DELAY_SEC: int = Field(default=1)

    RESPONSE_PROMPT_FILEPATH: str = Field(
        default="../data/prompts/default_response_prompt.yaml"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Vector Store
# ------------------------------------------------------------------
class VectorStoreSettings(BaseSettings):
    VECTOR_DB_FILE_PATH: str = Field(default="../data/db/vector_index.faiss")
    METADATA_DB_FILE_PATH: str = Field(default="../data/db/metadata.pkl")

    CHUNK_SIZE: int = Field(default=1000)
    CHUNK_OVERLAP: int = Field(default=20)

    RETRIEVAL_TOP_K: int = Field(default=3)
    SIMILARITY_THRESHOLD: float = Field(default=0.7)

    MAX_VECTORS_IN_MEMORY: int = Field(default=10000)
    VECTOR_BATCH_SIZE: int = Field(default=100)
    EMBEDDING_CACHE_ENABLED: bool = Field(default=True)
    EMBEDDING_CACHE_DIR: str = Field(default="../data/cache/embeddings")
    MAX_CACHE_SIZE_MB: int = Field(default=500)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Web Search
# ------------------------------------------------------------------
class WebSearchSettings(BaseSettings):
    IS_WEB_SEARCH_ENABLED: bool = Field(default=False)
    # SEARCH_API_KEY: SecretStr = Field(default=..., env="SEARCH_API_KEY")
    # SEARCH_ENGINE_ID: SecretStr = Field(default=..., env="SEARCH_ENGINE_ID")

    MAX_WEB_SEARCH_RESULTS: int = Field(default=5)
    WEB_REQUEST_TIMEOUT_SECS: int = Field(default=15)
    WEB_REQUEST_DELAY_SECS: int = Field(default=1)

    WEB_USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/91.0.4472.124 Safari/537.36"
    )

    MAX_WEB_CONTENT_LENGTH: int = Field(default=10000)
    MIN_WEB_CONTENT_LENGTH: int = Field(default=100)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------
class LoggingSettings(BaseSettings):
    LOG_LEVEL: str = Field(default="INFO")
    LOG_DIRECTORY: str = Field(default="../../../logs")
    LOG_FORMAT: str = Field(default="%(asctime)s [%(levelname)s]: %(message)s")
    DATE_FORMAT: str = Field(default="%Y-%m-%dT%H:%M:%S")
    IS_FILE_LOGGING_ENABLED: bool = Field(default=False)
    LOG_MAX_BYTES: int = Field(default=10485760)

    LOG_WEB_SEARCHES: bool = Field(default=False)
    LOG_DATABASE_QUERIES: bool = Field(default=False)
    LOG_API_REQUESTS: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# API Server
# ------------------------------------------------------------------
class APIServerSettings(BaseSettings):
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    WORKERS: int = Field(default=1)

    API_V1_PREFIX: str = Field(default="/api/v1")
    DOCS_URL: str = Field(default="/docs")
    REDOC_URL: str = Field(default="/redoc")

    CORS_ORIGINS: List[str] = Field(default=["http://localhost:3000"])
    CORS_ALLOW_CREDENTIALS: bool = Field(default=True)
    CORS_ALLOW_METHODS: List[str] = Field(default=["*"])
    CORS_ALLOW_HEADERS: List[str] = Field(default=["*"])

    RATE_LIMIT_ENABLED: bool = Field(default=True)
    RATE_LIMIT_REQUESTS: int = Field(default=100)
    RATE_LIMIT_WINDOW: int = Field(default=60)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Monitoring
# ------------------------------------------------------------------
class MonitoringSettings(BaseSettings):
    ENABLE_METRICS: bool = Field(default=True)
    METRICS_ENDPOINT: str = Field(default="/metrics")

    # SENTRY_DSN: Optional[SecretStr] = Field(default=None, env="SENTRY_DSN")
    SENTRY_ENVIRONMENT: str = Field(default="development")

    QA_SQLITE_DB_PATH: str = Field(default="../data/db/qa_log.db")
    ENABLE_EVALUATION_LOGGING: bool = Field(default=False)

    HEALTH_CHECK_TIMEOUT: int = Field(default=30)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# ------------------------------------------------------------------
# Main Settings Container
# ------------------------------------------------------------------
class Settings(BaseSettings):
    app: CoreAppSettings = CoreAppSettings()
    database: DatabaseSettings = DatabaseSettings()
    auth: AuthSettings = AuthSettings()
    files: FileProcessingSettings = FileProcessingSettings()
    llm: LLMIntegrationSettings = LLMIntegrationSettings()
    vector: VectorStoreSettings = VectorStoreSettings()
    web_search: WebSearchSettings = WebSearchSettings()
    logging: LoggingSettings = LoggingSettings()
    server: APIServerSettings = APIServerSettings()
    monitoring: MonitoringSettings = MonitoringSettings()

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


# Global settings instance
settings = Settings()


if __name__ == "__main__":
    db_url = settings.database.DATABASE_URL.get_secret_value()

    print(db_url)
