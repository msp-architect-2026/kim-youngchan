from fastapi import APIRouter, HTTPException, status
from typing import List
import uuid
import logging
from datetime import datetime

from app.schemas.order import (
    ReserveRequest, ReserveResponse,
    ConfirmRequest, ConfirmResponse,
    OrderResponse, OrderListResponse, OrderStatus
)
from app.core.dependencies import DBConnection, RedisClient
from app.core.auth import AuthUser
from app.db import queries
from app.metrics import order_reserve_total, order_confirm_total

router = APIRouter(prefix="/orders", tags=["orders"])
logger = logging.getLogger(__name__)


@router.post("/reserve", response_model=ReserveResponse)
async def reserve_order(
    request: ReserveRequest,
    current_user: AuthUser,
    db_conn: DBConnection,
    redis: RedisClient,
):
    from app.core.redis_client import redis_client

    sneaker_id = request.sneaker_id
    size_key = str(int(request.size)) if request.size == int(request.size) else str(request.size)
    user_id = current_user.user_id

    lock_key = f"order:lock:{sneaker_id}:{user_id}"
    lock_acquired = await redis.set(lock_key, "1", nx=True, ex=300)
    if not lock_acquired:
        order_reserve_total.labels(status="duplicate").inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 선점 중인 주문이 있습니다."
        )

    stock_key = f"stock:{sneaker_id}:{size_key}"
    try:
        result = await redis.evalsha(
            redis_client.reserve_sha,
            1,
            stock_key,
            "1"
        )
    except Exception as e:
        await redis.delete(lock_key)
        logger.error(f"Lua script error: {e}")
        order_reserve_total.labels(status="error").inc()
        raise HTTPException(status_code=500, detail="재고 처리 중 오류가 발생했습니다.")

    if result == 0:
        await redis.delete(lock_key)
        order_reserve_total.labels(status="out_of_stock").inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="재고가 부족합니다."
        )

    reserve_token = str(uuid.uuid4()).replace("-", "")
    token_key = f"reserve:token:{reserve_token}"
    token_value = f"{user_id}:{sneaker_id}:{size_key}"
    await redis.set(token_key, token_value, ex=180)
    await redis.incr("metrics:drop:success")

    order_reserve_total.labels(status="success").inc()
    logger.info(f"Reserve success: user={user_id}, sneaker={sneaker_id}, size={size_key}")

    return ReserveResponse(
        success=True,
        message="선점 성공",
        reserve_token=reserve_token,
        expires_in=180
    )


@router.post("/confirm", response_model=ConfirmResponse)
async def confirm_order(
    request: ConfirmRequest,
    current_user: AuthUser,
    db_conn: DBConnection,
    redis: RedisClient,
):
    from app.core.redis_client import redis_client

    user_id = current_user.user_id
    token_key = f"reserve:token:{request.reserve_token}"

    token_value = await redis.get(token_key)
    if not token_value:
        order_confirm_total.labels(status="invalid_token").inc()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="유효하지 않거나 만료된 선점 토큰입니다."
        )

    parts = token_value.split(":")
    if len(parts) != 3:
        raise HTTPException(status_code=400, detail="토큰 형식 오류")

    token_user_id, sneaker_id, size_key = int(parts[0]), int(parts[1]), parts[2]

    if token_user_id != user_id:
        order_confirm_total.labels(status="unauthorized").inc()
        raise HTTPException(status_code=403, detail="본인의 선점 토큰이 아닙니다.")

    lock_key = f"order:lock:{sneaker_id}:{user_id}"

    async with db_conn.cursor() as check_cursor:
        await check_cursor.execute(
            "SELECT id FROM orders WHERE user_id=%s AND sneaker_id=%s AND size=%s LIMIT 1",
            (user_id, sneaker_id, size_key)
        )
        if await check_cursor.fetchone():
            await redis.delete(token_key, lock_key)
            order_confirm_total.labels(status="duplicate").inc()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 구매한 상품입니다."
            )

    try:
        await db_conn.begin()
        async with db_conn.cursor() as cursor:
            await cursor.execute(queries.INSERT_ORDER, (
                user_id,
                sneaker_id,
                size_key,
                OrderStatus.CONFIRMED.value,
                request.reserve_token,
                datetime.utcnow()
            ))
            order_id = cursor.lastrowid
            await cursor.execute(queries.DECREMENT_DB_STOCK, (sneaker_id, size_key))
        await db_conn.commit()

    except Exception as e:
        await db_conn.rollback()
        logger.error(f"Confirm transaction failed: {e}")

        stock_key = f"stock:{sneaker_id}:{size_key}"
        try:
            await redis.evalsha(redis_client.rollback_sha, 1, stock_key, "1")
        except Exception as rollback_err:
            logger.critical(f"CRITICAL: Redis rollback failed: {rollback_err}, stock_key={stock_key}")

        order_confirm_total.labels(status="error").inc()
        raise HTTPException(status_code=500, detail="주문 확정 중 오류가 발생했습니다.")

    await redis.delete(token_key, lock_key)
    await redis.incr("metrics:drop:confirmed")

    order_confirm_total.labels(status="success").inc()
    logger.info(f"Confirm success: user={user_id}, order_id={order_id}")

    return ConfirmResponse(
        success=True,
        message="주문이 확정되었습니다.",
        order_id=order_id
    )


@router.get("", response_model=OrderListResponse)
async def get_my_orders(
    current_user: AuthUser,
    db_conn: DBConnection,
):
    async with db_conn.cursor() as cursor:
        await cursor.execute(queries.GET_ORDERS_BY_USER, (current_user.user_id, 50, 0))
        rows = await cursor.fetchall()

    orders = [
        OrderResponse(
            id=row[0],
            user_id=row[1],
            sneaker_id=row[2],
            size=float(row[3]),
            status=OrderStatus(row[4]),
            reserve_token=row[5],
            created_at=row[6],
            updated_at=row[7]
        )
        for row in rows
    ]

    return OrderListResponse(total=len(orders), orders=orders)