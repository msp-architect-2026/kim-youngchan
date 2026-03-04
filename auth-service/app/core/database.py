from __future__ import annotations

import aiomysql
import redis.asyncio as aioredis
from fastapi import FastAPI

from app.core.config import get_settings

settings = get_settings()

# ---------------------------------------------------------------------------
# MySQL
# ---------------------------------------------------------------------------

_mysql_pool: aiomysql.Pool | None = None


async def create_mysql_pool() -> None:
    global _mysql_pool
    _mysql_pool = await aiomysql.create_pool(
        host=settings.mysql_host,
        port=settings.mysql_port,
        user=settings.mysql_user,
        password=settings.mysql_password,
        db=settings.mysql_db,
        minsize=settings.mysql_pool_minsize,
        maxsize=settings.mysql_pool_maxsize,
        autocommit=False,
        charset="utf8mb4",
        connect_timeout=5,
    )


async def close_mysql_pool() -> None:
    if _mysql_pool:
        _mysql_pool.close()
        await _mysql_pool.wait_closed()


def get_mysql_pool() -> aiomysql.Pool:
    if _mysql_pool is None:
        raise RuntimeError("MySQL pool not initialized")
    return _mysql_pool


# ---------------------------------------------------------------------------
# Redis
# ---------------------------------------------------------------------------

_redis_client: aioredis.Redis | None = None


async def create_redis_client() -> None:
    global _redis_client
    _redis_client = aioredis.Redis(
        host=settings.redis_host,
        port=settings.redis_port,
        password=settings.redis_password or None,
        db=settings.redis_db,
        decode_responses=True,
        max_connections=100,
        socket_connect_timeout=3,
        socket_timeout=3,
        retry_on_timeout=True,
    )
    await _redis_client.ping()


async def close_redis_client() -> None:
    if _redis_client:
        await _redis_client.aclose()


def get_redis_client() -> aioredis.Redis:
    if _redis_client is None:
        raise RuntimeError("Redis client not initialized")
    return _redis_client


# ---------------------------------------------------------------------------
# FastAPI Depends helpers
# ---------------------------------------------------------------------------

async def get_db() -> aiomysql.Pool:
    return get_mysql_pool()


async def get_redis() -> aioredis.Redis:
    return get_redis_client()


# ---------------------------------------------------------------------------
# Lifespan hooks
# ---------------------------------------------------------------------------

async def startup(app: FastAPI) -> None:  # noqa: ARG001
    await create_mysql_pool()
    await create_redis_client()
    await _ensure_schema()


async def shutdown(app: FastAPI) -> None:  # noqa: ARG001
    await close_mysql_pool()
    await close_redis_client()


async def _ensure_schema() -> None:
    pool = get_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                    email         VARCHAR(255)    NOT NULL,
                    password_hash VARCHAR(255)    NOT NULL,
                    name          VARCHAR(100)    NOT NULL,
                    role          ENUM('USER','ADMIN') NOT NULL DEFAULT 'USER',
                    created_at    DATETIME        NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id),
                    UNIQUE KEY uq_users_email (email)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
                """
            )
        await conn.commit()