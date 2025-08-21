"""
Configuration settings for the DocuChatAPI application.
Each configuration class handles a specific domain of settings.
"""

import os
from pathlib import Path
from typing import List, Optional

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parent.parent.parent.parent / ".env"
PROD_ENV_FILE = ""


class CoreAppSettings(BaseSettings):
    """
    Core application settings that define the basic runtime environment
    and general application behavior.

    These settings control the fundamental aspects of the application
    such as environment mode and basic operational parameters.
    """

    ENV: str = Field(default="development", env="ENV")
    APP_NAME: str = Field(default="DocuChatAPI")
    DEBUG_ENABLED: bool = Field(default=True)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class DatabaseSettings(BaseSettings):
    """
    Database configuration settings for PostgresSQL and related database operations.

    Handles all database connection parameters, pool settings, and database-specific
    configurations for the main application database.
    """

    DATABASE_URL: Optional[SecretStr] = Field(default=None, env="DATABASE_URL")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: int = Field(default=5432, env="DB_PORT")
    DB_NAME: str = Field(default="docu_chat", env="DB_NAME")
    DB_USER: str = Field(default="postgres", env="DB_USER")
    DB_PASSWORD: SecretStr = Field(default="", env="DB_PASSWORD")

    # Connection Pool Settings
    DB_POOL_SIZE: int = Field(default=10)
    DB_MAX_OVERFLOW: int = Field(default=20)
    DB_ECHO: bool = Field(
        default=False, description="Echo SQL statements for debugging"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class AuthSettings(BaseSettings):
    """
    Authentication and authorization configuration settings.

    Manages JWT token configuration, password hashing parameters,
    and session management settings for user authentication.
    """

    # JWT Configuration
    ACCESS_SECRET: SecretStr = Field(env="ACCESS_TOKEN_SECRET")
    REFRESH_SECRET: SecretStr = Field(env="REFRESH_TOKEN_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=5)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class FileProcessingSettings(BaseSettings):
    """
    File upload and document processing configuration.

    Controls file upload limits, allowed file types, storage locations,
    and document processing parameters for the document management system.
    """

    # File Upload Configuration
    ALLOWED_FILE_EXTENSIONS: List[str] = Field(
        default=[".pdf", ".docx", ".txt", ".md"],
    )
    MAX_FILE_SIZE_MB: int = Field(default=20)
    MAX_FILES_PER_UPLOAD: int = Field(
        default=10, description="Maximum number of files per upload request"
    )

    # Storage Paths
    RAW_DOCS_DIRECTORY: str = Field(
        default="../data/raw_docs",
        description="Directory for storing raw uploaded documents",
    )
    PROCESSED_DOCS_DIRECTORY: str = Field(
        default="../data/processed_docs",
        description="Directory for processed documents",
    )

    # File Type Constants
    MD_FILE_EXT: str = Field(default=".md", description="Markdown file extension")
    TXT_FILE_EXT: str = Field(default=".txt", description="Text file extension")
    PDF_FILE_EXT: str = Field(default=".pdf", description="PDF file extension")
    DOCX_FILE_EXT: str = Field(
        default=".docx", description="Word document file extension"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class LLMIntegrationSettings(BaseSettings):
    """
    Large Language Model integration settings for AI/ML operations.

    Configures OpenAI API settings, model parameters, prompt configurations,
    and other LLM-related operational parameters.
    """

    # OpenAI API Configuration
    OPENAI_API_KEY: SecretStr = Field(
        env="OPENAI_API_KEY", description="OpenAI API key for LLM access"
    )
    LLM_MODEL_NAME: str = Field(
        default="gpt-3.5-turbo", description="OpenAI model name for chat completions"
    )
    EMBEDDING_MODEL_NAME: str = Field(
        default="text-embedding-3-small", description="OpenAI model for text embeddings"
    )

    # Model Parameters
    LLM_TEMPERATURE: float = Field(
        default=0.7, description="Temperature setting for LLM responses (0.0 - 2.0)"
    )
    MAX_TOKENS: int = Field(
        default=4096, description="Maximum tokens for LLM responses"
    )

    # API Rate Limiting and Reliability
    OPENAI_API_RATE_LIMIT: int = Field(
        default=60, description="API requests per minute limit"
    )
    OPENAI_API_TIMEOUT_SEC: int = Field(
        default=30, description="API request timeout in seconds"
    )
    MAX_API_RETRIES: int = Field(
        default=3, description="Maximum retry attempts for failed API calls"
    )
    API_RETRY_DELAY_SEC: int = Field(
        default=1, description="Delay between API retry attempts"
    )

    # Prompt Configuration
    RESPONSE_PROMPT_FILEPATH: str = Field(
        default="../data/prompts/default_response_prompt.yaml",
        description="Path to the default response prompt template file",
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class VectorStoreSettings(BaseSettings):
    """
    Vector database and embedding storage configuration.

    Manages FAISS vector store settings, embedding parameters, chunking strategy,
    and vector search configurations for the RAG system.
    """

    # Vector Database Paths
    VECTOR_DB_FILE_PATH: str = Field(
        default="../data/db/vector_index.faiss",
        description="Path to FAISS vector index file",
    )
    METADATA_DB_FILE_PATH: str = Field(
        default="../data/db/metadata.pkl",
        description="Path to vector metadata pickle file",
    )

    # Document Chunking Strategy
    CHUNK_SIZE: int = Field(
        default=1000, description="Size of document chunks for embedding"
    )
    CHUNK_OVERLAP: int = Field(
        default=20, description="Overlap between consecutive chunks"
    )

    # Vector Search Configuration
    RETRIEVAL_TOP_K: int = Field(
        default=3, description="Number of top documents to retrieve for RAG"
    )
    SIMILARITY_THRESHOLD: float = Field(
        default=0.7, description="Minimum similarity threshold for relevant chunks"
    )

    # Performance and Caching
    MAX_VECTORS_IN_MEMORY: int = Field(
        default=10000, description="Maximum vectors to keep in memory"
    )
    VECTOR_BATCH_SIZE: int = Field(
        default=100, description="Batch size for vector operations"
    )
    EMBEDDING_CACHE_ENABLED: bool = Field(
        default=True, description="Enable embedding caching"
    )
    EMBEDDING_CACHE_DIR: str = Field(
        default="../data/cache/embeddings", description="Directory for embedding cache"
    )
    MAX_CACHE_SIZE_MB: int = Field(
        default=500, description="Maximum cache size in megabytes"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class WebSearchSettings(BaseSettings):
    """
    Web search integration configuration for enhanced RAG capabilities.

    Controls web search API settings, search parameters, content processing,
    and web scraping configurations when web search is enabled.
    """

    # Web Search Toggle
    IS_WEB_SEARCH_ENABLED: bool = Field(
        default=False, description="Enable web search functionality"
    )

    # Search API Configuration
    SEARCH_API_KEY: Optional[SecretStr] = Field(
        default=None, env="SEARCH_API_KEY", description="Google Custom Search API key"
    )
    SEARCH_ENGINE_ID: Optional[SecretStr] = Field(
        default=None,
        env="SEARCH_ENGINE_ID",
        description="Google Custom Search Engine ID",
    )

    # Search Parameters
    MAX_WEB_SEARCH_RESULTS: int = Field(
        default=5, description="Maximum number of web search results to process"
    )

    # Web Request Configuration
    WEB_REQUEST_TIMEOUT_SECS: int = Field(
        default=15, description="Timeout for web requests in seconds"
    )
    WEB_REQUEST_DELAY_SECS: int = Field(
        default=1, description="Delay between web requests to avoid rate limiting"
    )
    WEB_USER_AGENT: str = Field(
        default="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        description="User agent string for web requests",
    )

    # Content Processing
    MAX_WEB_CONTENT_LENGTH: int = Field(
        default=10000, description="Maximum length of web content to process"
    )
    MIN_WEB_CONTENT_LENGTH: int = Field(
        default=100, description="Minimum length of web content to consider"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class LoggingSettings(BaseSettings):
    """
    Logging configuration for application monitoring and debugging.

    Controls log levels, output destinations, log formatting, and specific
    logging behaviors for different application components.
    """

    # Log Level Configuration
    LOG_LEVEL: str = Field(
        default="INFO",
        description="Application log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
    )
    ROOT_LOG_LEVEL: str = Field(
        default="WARNING",
        description="Root logger level to control third-party library logging",
    )

    # Log Output Configuration
    LOG_DIRECTORY: str = Field(default="../logs", description="Directory for log files")
    IS_FILE_LOGGING_ENABLED: bool = Field(
        default=True, description="Enable logging to files"
    )
    IS_CONSOLE_LOGGING_ENABLED: bool = Field(
        default=True, description="Enable console logging"
    )

    # Log Rotation
    LOG_MAX_BYTES: int = Field(
        default=10485760, description="Maximum log file size in bytes (10MB)"
    )
    LOG_BACKUP_COUNT: int = Field(
        default=5, description="Number of log backup files to keep"
    )

    # Specific Feature Logging
    LOG_WEB_SEARCHES: bool = Field(
        default=False, description="Enable detailed logging of web search operations"
    )
    LOG_DATABASE_QUERIES: bool = Field(
        default=False, description="Enable logging of database queries"
    )
    LOG_API_REQUESTS: bool = Field(
        default=True, description="Enable logging of API requests"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class APIServerSettings(BaseSettings):
    """
    API server configuration for FastAPI application setup.

    Controls server behavior, CORS settings, middleware configuration,
    and other web server related settings.
    """

    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host address")
    PORT: int = Field(default=8000, description="Server port number")
    WORKERS: int = Field(default=1, description="Number of worker processes")

    # API Configuration
    API_V1_PREFIX: str = Field(default="/api/v1", description="API version 1 prefix")
    DOCS_URL: str = Field(default="/docs", description="OpenAPI documentation URL")
    REDOC_URL: str = Field(default="/redoc", description="ReDoc documentation URL")

    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"], description="Allowed CORS origins"
    )
    CORS_ALLOW_CREDENTIALS: bool = Field(
        default=True, description="Allow credentials in CORS requests"
    )
    CORS_ALLOW_METHODS: List[str] = Field(
        default=["*"], description="Allowed HTTP methods for CORS"
    )
    CORS_ALLOW_HEADERS: List[str] = Field(
        default=["*"], description="Allowed headers for CORS"
    )

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = Field(
        default=True, description="Enable API rate limiting"
    )
    RATE_LIMIT_REQUESTS: int = Field(
        default=100, description="Number of requests per time window"
    )
    RATE_LIMIT_WINDOW: int = Field(
        default=60, description="Rate limit time window in seconds"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class MonitoringSettings(BaseSettings):
    """
    Application monitoring and analytics configuration.

    Controls performance monitoring, error tracking, metrics collection,
    and evaluation/testing database settings.
    """

    # Performance Monitoring
    ENABLE_METRICS: bool = Field(
        default=True, description="Enable application metrics collection"
    )
    METRICS_ENDPOINT: str = Field(
        default="/metrics", description="Prometheus metrics endpoint"
    )

    # Error Tracking
    SENTRY_DSN: Optional[SecretStr] = Field(
        default=None, env="SENTRY_DSN", description="Sentry DSN for error tracking"
    )
    SENTRY_ENVIRONMENT: str = Field(
        default="development", description="Sentry environment name"
    )

    # Evaluation and Testing
    QA_SQLITE_DB_PATH: str = Field(
        default="../data/db/qa_log.db",
        description="SQLite database path for Q&A evaluation logs",
    )
    ENABLE_EVALUATION_LOGGING: bool = Field(
        default=False, description="Enable logging of Q&A pairs for evaluation"
    )

    # Health Checks
    HEALTH_CHECK_TIMEOUT: int = Field(
        default=30, description="Health check timeout in seconds"
    )

    model_config = SettingsConfigDict(env_file=ENV_FILE, extra="ignore")


class Settings(BaseSettings):
    """
    Main settings container that aggregates all configuration classes.

    Provides a single point of access to all application settings
    while maintaining logical separation of different configuration domains.
    """

    # Core Configuration Groups
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
