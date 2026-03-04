from fastapi import Depends, HTTPException, Header
from typing import Annotated
import redis.asyncio as aioredis
import aiomysql

from app.core.database import db
from app.core.redis_client import redis_client
from app.core.config import get_settings

settings = get_settings()


async def get_db_connection():
    """Get MySQL database connection"""
    async with db.get_connection() as conn:
        yield conn


async def get_redis() -> aioredis.Redis:
    """Get Redis client"""
    return redis_client.get_client()


async def verify_admin_key(x_admin_key: Annotated[str, Header()]) -> bool:
    """Verify admin API key"""
    if x_admin_key != settings.ADMIN_SECRET_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin key")
    return True


# Type aliases for dependency injection
DBConnection = Annotated[aiomysql.Connection, Depends(get_db_connection)]
RedisClient = Annotated[aioredis.Redis, Depends(get_redis)]
AdminAuth = Annotated[bool, Depends(verify_admin_key)]