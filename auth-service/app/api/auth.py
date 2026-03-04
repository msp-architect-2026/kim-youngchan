from __future__ import annotations

from typing import Annotated

import aiomysql
import redis.asyncio as aioredis
from fastapi import APIRouter, Depends, HTTPException, status

from app.core.database import get_db, get_redis
from app.core.dependencies import get_current_user
from app.core.security import (
    create_access_token,
    hash_password,
    remaining_ttl,
    verify_password,
)
from app.schemas.auth import (
    LoginRequest,
    MessageResponse,
    SignupRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# POST /api/auth/signup
# ---------------------------------------------------------------------------

@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def signup(
    body: SignupRequest,
    pool: Annotated[aiomysql.Pool, Depends(get_db)],
) -> dict:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT id FROM users WHERE email = %s", (body.email,)
            )
            if await cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already registered",
                )

            await cur.execute(
                """
                INSERT INTO users (email, password_hash, name, role)
                VALUES (%s, %s, %s, 'USER')
                """,
                (body.email, hash_password(body.password), body.name),
            )
            await conn.commit()
            new_id = cur.lastrowid

            await cur.execute(
                "SELECT id, email, name, role, created_at FROM users WHERE id = %s",
                (new_id,),
            )
            user = await cur.fetchone()

    return user


# ---------------------------------------------------------------------------
# POST /api/auth/login
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    pool: Annotated[aiomysql.Pool, Depends(get_db)],
) -> dict:
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(
                "SELECT id, password_hash, role FROM users WHERE email = %s",
                (body.email,),
            )
            user = await cur.fetchone()

    if not user or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token, _jti, exp = create_access_token(user["id"], user["role"])

    return {
        "access_token": token,
        "token_type": "bearer",
        "expires_in": remaining_ttl(exp),
    }


# ---------------------------------------------------------------------------
# GET /api/auth/me
# ---------------------------------------------------------------------------

@router.get("/me", response_model=UserResponse)
async def me(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> dict:
    return current_user


# ---------------------------------------------------------------------------
# POST /api/auth/logout
# ---------------------------------------------------------------------------

@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: Annotated[dict, Depends(get_current_user)],
    redis: Annotated[aioredis.Redis, Depends(get_redis)],
) -> dict:
    payload = current_user["_payload"]
    jti: str = payload["jti"]
    ttl = remaining_ttl(payload["exp"])

    if ttl > 0:
        await redis.set(f"blacklist:{jti}", "1", ex=ttl)

    return {"message": "Successfully logged out"}