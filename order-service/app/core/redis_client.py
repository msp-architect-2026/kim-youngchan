import redis.asyncio as aioredis
import os
import logging
from typing import Optional

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self):
        self.pool: Optional[aioredis.ConnectionPool] = None
        self.client: Optional[aioredis.Redis] = None
        
        # Lua script SHA hashes
        self.reserve_sha: str = ""
        self.rollback_sha: str = ""
        
        # Lua scripts content
        self.lua_reserve: str = ""
        self.lua_rollback: str = ""
    
    def _load_lua_scripts(self):
        """Load Lua scripts from files"""
        lua_dir = os.path.join(os.path.dirname(__file__), "../lua")
        
        with open(os.path.join(lua_dir, "reserve_stock.lua"), "r") as f:
            self.lua_reserve = f.read()
        
        with open(os.path.join(lua_dir, "rollback_stock.lua"), "r") as f:
            self.lua_rollback = f.read()
    
    async def connect(self):
        """Initialize Redis connection pool and load Lua scripts"""
        try:
            self.pool = aioredis.ConnectionPool(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                password=settings.REDIS_PASSWORD if settings.REDIS_PASSWORD else None,
                max_connections=settings.REDIS_POOL_SIZE,
                decode_responses=True
            )
            self.client = aioredis.Redis(connection_pool=self.pool)
            
            # Test connection
            await self.client.ping()
            
            # Load Lua scripts
            self._load_lua_scripts()
            self.reserve_sha = await self.client.script_load(self.lua_reserve)
            self.rollback_sha = await self.client.script_load(self.lua_rollback)
            
            logger.info(f"Redis connected. Lua scripts loaded: reserve={self.reserve_sha[:8]}..., rollback={self.rollback_sha[:8]}...")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Close Redis connection"""
        if self.client:
            await self.client.close()
        if self.pool:
            await self.pool.disconnect()
        logger.info("Redis connection closed")
    
    def get_client(self) -> aioredis.Redis:
        """Get Redis client instance"""
        if not self.client:
            raise RuntimeError("Redis client not initialized")
        return self.client


# Global Redis instance
redis_client = RedisClient()