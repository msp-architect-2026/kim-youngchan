"""
MySQL database connection management with aiomysql
Async connection pool with graceful shutdown
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

from app.core.config import settings

logger = logging.getLogger(__name__)

# SQLAlchemy Base
Base = declarative_base()

# Global engine and session maker
_engine = None
_async_session_maker = None


async def init_db():
    """Initialize async database engine and session maker"""
    global _engine, _async_session_maker
    
    logger.info("Initializing database connection pool")
    logger.info(
        f"Pool configuration: pool_size={settings.db_pool_size}, "
        f"max_overflow={settings.db_max_overflow}"
    )
    
    _engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,  # Verify connections before using
        pool_size=settings.db_pool_size,
        max_overflow=settings.db_max_overflow,
        pool_recycle=3600,  # Recycle connections every hour
        pool_timeout=30,
        connect_args={
            "connect_timeout": 10,
        }
    )
    
    _async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )
    
    logger.info("Database connection pool initialized successfully")


async def close_db():
    """Gracefully close database connections"""
    global _engine
    
    if _engine:
        logger.info("Closing database connection pool")
        await _engine.dispose()
        logger.info("Database connection pool closed")


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Database session dependency
    
    Usage:
        async with get_db() as session:
            result = await session.execute(query)
    """
    if not _async_session_maker:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    
    async with _async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_health() -> bool:
    """Check database connection health"""
    try:
        async with get_db() as session:
            result = await session.execute(text("SELECT 1"))
            result.scalar()
        return True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return False