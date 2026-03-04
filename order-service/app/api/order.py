from fastapi import APIRouter, HTTPException, Query
import secrets
import logging
from datetime import datetime
from typing import Optional

from app.schemas.order import (
    ReserveRequest, ReserveResponse,
    ConfirmRequest, ConfirmResponse,
    OrderResponse, OrderListResponse, OrderStatus
)
from app.core.dependencies import DBConnection, RedisClient
from app.core.config import get_settings
from app.core.redis_client import redis_client
from app.db import queries

router = APIRouter(prefix="/orders", tags=["orders"])
settings = get_settings()
logger = logging.getLogger(__name__)


# ============= Helper Functions =============

def stock_key(sneaker_id: int, size: float) -> str:
    """Generate Redis stock key"""
    return f"stock:{sneaker_id}:{int(size)}"


def lock_key(sneaker_id: int, user_id: int) -> str:
    """Generate Redis lock key"""
    return f"order:lock:{sneaker_id}:{user_id}"


def token_key(token: str) -> str:
    """Generate Redis token key"""
    return f"reserve:token:{token}"


def generate_token() -> str:
    """Generate secure reserve token"""
    return secrets.token_urlsafe(32)


# ============= API Endpoints =============

@router.post("/reserve", response_model=ReserveResponse)
async def reserve_stock(
    request: ReserveRequest,
    redis: RedisClient
):
    """
    Reserve stock atomically using Redis Lua script
    
    Flow:
    1. Acquire distributed lock (SETNX)
    2. Execute Lua script: check stock -> decrement
    3. Generate reserve_token with TTL
    4. Return token to user
    """
    user_id = request.user_id
    sneaker_id = request.sneaker_id
    size = request.size
    
    # Step 1: Acquire lock
    lock = lock_key(sneaker_id, user_id)
    lock_acquired = await redis.set(
        lock, "1", nx=True, ex=settings.ORDER_LOCK_TTL
    )
    
    if not lock_acquired:
        return ReserveResponse(
            success=False,
            message="Duplicate request detected. Please wait.",
            reserve_token=None,
            expires_in=None
        )
    
    try:
        # Step 2: Execute Lua script for atomic stock reservation
        stock = stock_key(sneaker_id, size)
        result = await redis.evalsha(
            redis_client.reserve_sha,
            1,  # number of keys
            stock,  # KEYS[1]
            1  # ARGV[1] - quantity
        )
        
        if result == 0:
            await redis.delete(lock)
            return ReserveResponse(
                success=False,
                message="Out of stock",
                reserve_token=None,
                expires_in=None
            )
        
        # Step 3: Generate and store reserve token
        token = generate_token()
        token_data = f"{user_id}:{sneaker_id}:{size}"
        await redis.setex(
            token_key(token),
            settings.RESERVE_TOKEN_TTL,
            token_data
        )
        
        logger.info(f"Reserved - User:{user_id}, Sneaker:{sneaker_id}, Size:{size}, Token:{token[:8]}...")
        
        return ReserveResponse(
            success=True,
            message="Stock reserved successfully",
            reserve_token=token,
            expires_in=settings.RESERVE_TOKEN_TTL
        )
        
    except Exception as e:
        logger.error(f"Reserve error: {e}")
        await redis.delete(lock)
        return ReserveResponse(
            success=False,
            message="Internal error during reservation",
            reserve_token=None,
            expires_in=None
        )


@router.post("/confirm", response_model=ConfirmResponse)
async def confirm_order(
    request: ConfirmRequest,
    db_conn: DBConnection,
    redis: RedisClient
):
    """
    Confirm order and persist to MySQL
    
    Flow:
    1. Validate reserve_token from Redis
    2. Begin MySQL transaction
    3. INSERT into orders table
    4. Commit transaction
    5. Delete token and release lock
    6. On failure: rollback stock in Redis
    """
    token = request.reserve_token
    
    # Step 1: Validate token
    token_data = await redis.get(token_key(token))
    if not token_data:
        return ConfirmResponse(
            success=False,
            message="Invalid or expired reserve token",
            order_id=None
        )
    
    try:
        # Parse token data
        parts = token_data.split(":")
        user_id = int(parts[0])
        sneaker_id = int(parts[1])
        size = float(parts[2])
    except (ValueError, IndexError):
        return ConfirmResponse(
            success=False,
            message="Corrupted reserve token",
            order_id=None
        )
    
    # Step 2-4: Insert into MySQL
    async with db_conn.cursor() as cursor:
        try:
            await db_conn.begin()
            
            await cursor.execute(queries.INSERT_ORDER, (
                user_id,
                sneaker_id,
                size,
                OrderStatus.CONFIRMED.value,
                token,
                datetime.utcnow()
            ))
            
            order_id = cursor.lastrowid
            await db_conn.commit()
            
            # Step 5: Cleanup
            await redis.delete(token_key(token))
            await redis.delete(lock_key(sneaker_id, user_id))
            
            logger.info(f"Confirmed - OrderID:{order_id}, User:{user_id}, Sneaker:{sneaker_id}")
            
            return ConfirmResponse(
                success=True,
                message="Order confirmed successfully",
                order_id=order_id
            )
            
        except Exception as e:
            await db_conn.rollback()
            
            # Step 6: Rollback stock
            stock = stock_key(sneaker_id, size)
            await redis.evalsha(
                redis_client.rollback_sha,
                1,
                stock,
                1
            )
            await redis.delete(lock_key(sneaker_id, user_id))
            
            logger.error(f"Confirm error: {e}")
            
            if "Duplicate entry" in str(e) or "uk_user_product_size" in str(e):
                return ConfirmResponse(
                    success=False,
                    message="You have already ordered this item",
                    order_id=None
                )
            
            return ConfirmResponse(
                success=False,
                message="Failed to confirm order",
                order_id=None
            )


@router.get("", response_model=OrderListResponse)
async def get_orders(
    db_conn: DBConnection,
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    """
    Get orders list
    
    - If user_id provided: return user's orders
    - Otherwise: return all orders (admin view)
    """
    async with db_conn.cursor() as cursor:
        if user_id:
            # Get user's orders
            await cursor.execute(queries.COUNT_ORDERS_BY_USER, (user_id,))
            result = await cursor.fetchone()
            total = result[0] if result else 0
            
            await cursor.execute(queries.GET_ORDERS_BY_USER, (user_id, limit, offset))
        else:
            # Get all orders
            await cursor.execute(queries.COUNT_ALL_ORDERS)
            result = await cursor.fetchone()
            total = result[0] if result else 0
            
            await cursor.execute(queries.GET_ALL_ORDERS, (limit, offset))
        
        rows = await cursor.fetchall()
        
        orders = [
            OrderResponse(
                id=row[0],
                user_id=row[1],
                sneaker_id=row[2],
                size=row[3],
                status=OrderStatus(row[4]),
                reserve_token=row[5],
                created_at=row[6],
                updated_at=row[7]
            )
            for row in rows
        ]
        
        return OrderListResponse(total=total, orders=orders)