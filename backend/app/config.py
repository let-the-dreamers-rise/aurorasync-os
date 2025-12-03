"""
Configuration management for AuroraSync OS backend.
Uses pydantic-settings for environment variable management.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    Defaults are provided for local development.
    """
    
    # Database Configuration
    # Using SQLite for easy setup (no PostgreSQL installation needed)
    DATABASE_URL: str = "sqlite:///./aurorasync.db"
    # For PostgreSQL: "postgresql://postgres:postgres@localhost:5432/aurorasync"
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Application Configuration
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "development"
    
    # API Configuration
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AuroraSync OS"
    VERSION: str = "0.1.0"
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
    ]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )


# Global settings instance
settings = Settings()
