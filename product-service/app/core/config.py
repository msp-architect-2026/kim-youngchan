"""
Application configuration using pydantic-settings
Loads environment variables with DB_ prefix and other configs
"""
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "DropX Product Service"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database Configuration (DB_ prefix)
    db_user: str = Field(default="dropx", alias="DB_USER")
    db_password: str = Field(default="dropx123", alias="DB_PASSWORD")
    db_host: str = Field(default="mysql", alias="DB_HOST")
    db_port: int = Field(default=3306, alias="DB_PORT")
    db_name: str = Field(default="dropx", alias="DB_NAME")
    db_pool_size: int = Field(default=20, alias="DB_POOL_SIZE")
    db_max_overflow: int = Field(default=40, alias="DB_MAX_OVERFLOW")
    
    # Redis Configuration
    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")
    redis_max_connections: int = Field(default=100, alias="REDIS_MAX_CONNECTIONS")
    
    # Cache Configuration
    cache_ttl: int = Field(default=300, alias="CACHE_TTL")  # 5 minutes
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def database_url(self) -> str:
        """Construct MySQL async connection URL"""
        return f"mysql+aiomysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    @property
    def redis_url(self) -> str:
        """Construct Redis connection URL"""
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


@lru_cache()
def get_settings() -> Settings:
    """
    Cached settings instance
    Returns the same instance on subsequent calls
    """
    return Settings()


# Global settings instance
settings = get_settings()