import aiomysql
from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging

from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class Database:
    def __init__(self):
        self.pool: aiomysql.Pool | None = None
    
    async def connect(self):
        """Initialize MySQL connection pool"""
        try:
            self.pool = await aiomysql.create_pool(
                host=settings.MYSQL_HOST,
                port=settings.MYSQL_PORT,
                user=settings.MYSQL_USER,
                password=settings.MYSQL_PASSWORD,
                db=settings.MYSQL_DATABASE,
                minsize=settings.MYSQL_POOL_SIZE,
                maxsize=settings.MYSQL_POOL_SIZE + settings.MYSQL_MAX_OVERFLOW,
                autocommit=False,
                charset='utf8mb4'
            )
            logger.info("MySQL connection pool created")
        except Exception as e:
            logger.error(f"Failed to connect to MySQL: {e}")
            raise
    
    async def disconnect(self):
        """Close MySQL connection pool"""
        if self.pool:
            self.pool.close()
            await self.pool.wait_closed()
            logger.info("MySQL connection pool closed")
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[aiomysql.Connection, None]:
        """Get a connection from the pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as conn:
            yield conn


# Global database instance
db = Database()