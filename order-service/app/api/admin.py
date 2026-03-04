from fastapi import APIRouter, Query
import os
import sys
import asyncio
import logging
from typing import List

from app.schemas.order import (
    KillPodResponse, MetricsResponse, AdminOrderResponse, OrderStatus
)
from app.core.dependencies import DBConnection, AdminAuth
from app.db import queries

router = APIRouter(prefix="/admin", tags=["admin"])
logger = logging.getLogger(__name__)


@router.post("/kill-pod", response_model=KillPodResponse)
async def kill_pod(
    _: AdminAuth,
    exit_code: int = Query(1, description="Exit code for the process")
):
    """
    Gracefully kill current pod for chaos engineering
    
    Requires: X-Admin-Key header
    
    Use case:
    - Test K8s auto-recovery
    - Simulate pod failure
    - Trigger rolling update
    """
    pod_name = os.getenv("HOSTNAME", "unknown-pod")
    
    logger.warning(f"Admin kill-pod triggered for {pod_name} with exit_code={exit_code}")
    
    # Schedule exit after response is sent
    import signal
    asyncio.get_event_loop().call_later(0.5, lambda: os.kill(os.getpid(), signal.SIGTERM))
    
    return KillPodResponse(
        success=True,
        message=f"Pod {pod_name} will terminate in 0.5 seconds",
        pod_name=pod_name,
        exit_code=exit_code
    )


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics(
    _: AdminAuth,
    db_conn: DBConnection
):
    """
    Get order statistics and metrics
    
    Requires: X-Admin-Key header
    
    Returns:
    - Total orders by status
    - Success rate
    """
    async with db_conn.cursor() as cursor:
        # Get total orders
        await cursor.execute(queries.COUNT_ALL_ORDERS)
        result = await cursor.fetchone()
        total_orders = result[0] if result else 0
        
        # Get counts by status
        await cursor.execute(queries.COUNT_ORDERS_BY_STATUS)
        rows = await cursor.fetchall()
        
        status_counts = {
            "CONFIRMED": 0,
            "RESERVED": 0,
            "CANCELLED": 0,
            "FAILED": 0
        }
        
        for row in rows:
            status = row[0]
            count = row[1]
            status_counts[status] = count
        
        # Calculate success rate
        confirmed = status_counts["CONFIRMED"]
        success_rate = (confirmed / total_orders * 100) if total_orders > 0 else 0.0
        
        return MetricsResponse(
            total_orders=total_orders,
            confirmed_orders=status_counts["CONFIRMED"],
            reserved_orders=status_counts["RESERVED"],
            cancelled_orders=status_counts["CANCELLED"],
            failed_orders=status_counts["FAILED"],
            success_rate=round(success_rate, 2)
        )


@router.get("/orders", response_model=List[AdminOrderResponse])
async def get_admin_orders(
    _: AdminAuth,
    db_conn: DBConnection,
    status: OrderStatus = Query(None, description="Filter by status"),
    limit: int = Query(50, ge=1, le=1000)
):
    """
    Get orders for admin view with filters
    
    Requires: X-Admin-Key header
    
    Filters:
    - status: RESERVED, CONFIRMED, CANCELLED, FAILED
    - limit: max results
    """
    async with db_conn.cursor() as cursor:
        if status:
            query = """
                SELECT id, user_id, sneaker_id, size, status, created_at
                FROM orders
                WHERE status = %s
                ORDER BY created_at DESC
                LIMIT %s
            """
            await cursor.execute(query, (status.value, limit))
        else:
            query = """
                SELECT id, user_id, sneaker_id, size, status, created_at
                FROM orders
                ORDER BY created_at DESC
                LIMIT %s
            """
            await cursor.execute(query, (limit,))
        
        rows = await cursor.fetchall()
        
        orders = [
            AdminOrderResponse(
                order_id=row[0],
                user_id=row[1],
                sneaker_id=row[2],
                size=row[3],
                status=OrderStatus(row[4]),
                created_at=row[5]
            )
            for row in rows
        ]
        
        return orders