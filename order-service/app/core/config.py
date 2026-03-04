from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "dropx-order-service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # MySQL Configuration
    MYSQL_HOST: str = "mysql"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "dropx"
    MYSQL_PASSWORD: str = "dropx123"
    MYSQL_DATABASE: str = "dropx"
    MYSQL_POOL_SIZE: int = 20
    MYSQL_MAX_OVERFLOW: int = 10
    
    # Redis Configuration
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str = ""
    REDIS_POOL_SIZE: int = 50
    
    # Order Settings
    RESERVE_TOKEN_TTL: int = 180  # 3 minutes
    ORDER_LOCK_TTL: int = 300     # 5 minutes
    
    # Admin Settings
    ADMIN_SECRET_KEY: str = "change-this-in-production"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()