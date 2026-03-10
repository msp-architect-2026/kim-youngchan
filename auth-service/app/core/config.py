from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # JWT
    jwt_secret_key: str = "CHANGE_ME_IN_PRODUCTION_USE_256BIT_SECRET"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 43200

    # MySQL
    mysql_host: str = "mysql"
    mysql_port: int = 3306
    mysql_user: str = "dropx"
    mysql_password: str = "dropx_pass"
    mysql_db: str = "dropx"
    mysql_pool_minsize: int = 5
    mysql_pool_maxsize: int = 20

    # Redis
    redis_host: str = "redis"
    redis_port: int = 6379
    redis_password: str = ""
    redis_db: int = 0

    # App
    app_env: str = "production"
    metrics_port: int = 8001


@lru_cache
def get_settings() -> Settings:
    return Settings()