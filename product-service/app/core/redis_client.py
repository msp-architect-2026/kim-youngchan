"""
Redis connection management with redis.asyncio
Async connection pool with circuit breaker support
"""
import logging
from typing import Optional

import redis.asyncio as redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError

from app.core.config import settings

logger = logging.getLogger(__name__)

# Global Redis client
_redis_client: Optional[redis.Redis] = None


async def init_redis():
    """Initialize Redis connection pool"""
    global _redis_client
    
    logger.info(f"Initializing Redis connection pool: {settings.redis_url}")
    logger.info(f"Redis pool configuration: max_connections={settings.redis_max_connections}")
    
    _redis_client = redis.from_url(
        settings.redis_url,
        encoding="utf-8",
        decode_responses=True,
        max_connections=settings.redis_max_connections,
        socket_connect_timeout=5,
        socket_timeout=5,
        socket_keepalive=True,
        health_check_interval=30,
        retry_on_timeout=True,
    )
    
    # Health check
    try:
        await _redis_client.ping()
        logger.info("Redis connection established successfully")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")
        raise


async def close_redis():
    """Gracefully close Redis connections"""
    global _redis_client
    
    if _redis_client:
        logger.info("Closing Redis connection pool")
        await _redis_client.close()
        await _redis_client.connection_pool.disconnect()
        logger.info("Redis connection pool closed")


def get_redis() -> redis.Redis:
    """
    Get Redis client instance
    
    Returns:
        Redis client
        
    Raises:
        RuntimeError: If Redis not initialized
    """
    if not _redis_client:
        raise RuntimeError("Redis not initialized. Call init_redis() first.")
    
    return _redis_client


async def check_redis_health() -> bool:
    """Check Redis connection health"""
    try:
        client = get_redis()
        await client.ping()
        return True
    except Exception as e:
        logger.error(f"Redis health check failed: {e}")
        return False


class RedisKeyBuilder:
    @staticmethod
    def stock_key(sneaker_id: int, size: str) -> str:
        return f"stock:{sneaker_id}:{int(float(size))}"
    
    @staticmethod
    def sneaker_list_key() -> str:
        """Generate sneaker list cache key"""
        return "sneakers:list:active"