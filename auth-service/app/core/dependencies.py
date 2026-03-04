from __future__ import annotations

from typing import Annotated

import aiomysql
import redis.asyncio as aioredis
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError

from app.core.database import get_db, get_redis
from app.core.security import decode_token

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    redis: Annotated[aioredis.Redis, Depends(get_redis)],
    pool: Annotated[aiomysql.Pool, Depends(get_db)],
) -> dict:
    token = credentials.credentials
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 1. JWT 서명 / 만료 검증
    try:
        payload = decode_token(token)
    except JWTError:
        raise credentials_exception

    # 2. Redis 블랙리스트 선제 차단 (O(1))
    jti: str = payload.get("jti", "")
    if await redis.exists(f"blacklist:{jti}"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has been revoked",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. DB에서 유저 조회
    user_id = int(payload["sub"])
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT id, email, name, role, created_at FROM users WHERE id = %s",
                (user_id,),
            )
            user = await cur.fetchone()

    if not user:
        raise credentials_exception

    # logout / me 에서 사용할 내부 전용 필드
    user["_token"] = token
    user["_payload"] = payload
    return user