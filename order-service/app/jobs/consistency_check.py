"""
Consistency Check CronJob

Purpose:
- Cancel expired RESERVED orders that were never confirmed
- Restore stock in Redis for cancelled orders
- Run periodically (e.g., every 5 minutes)

Deployment:
- K8s CronJob
- Standalone script execution
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Tuple

from app.core.database import db
from app.core.redis_client import redis_client
from app.core.config import get_settings
from app.db import queries

settings = get_settings()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def stock_key(sneaker_id: int, size: float) -> str:
    return f"stock:{sneaker_id}:{int(size)}"  # stock:1:255


async def get_expired_reservations(
    batch_size: int = 100
) -> List[Tuple[int, int, int, float]]:
    """
    Get expired RESERVED orders from MySQL
    
    Returns: List of (order_id, user_id, sneaker_id, size)
    """
    expired_orders = []
    
    async with db.get_connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                queries.GET_EXPIRED_RESERVATIONS,
                (settings.RESERVE_TOKEN_TTL, batch_size)
            )
            rows = await cursor.fetchall()
            
            for row in rows:
                order_id = row[0]
                user_id = row[1]
                sneaker_id = row[2]
                size = row[3]
                expired_orders.append((order_id, user_id, sneaker_id, size))
    
    return expired_orders


async def cancel_order_and_restore_stock(
    order_id: int,
    sneaker_id: int,
    size: float
) -> bool:
    """
    Cancel order in MySQL and restore stock in Redis
    
    Returns: True if successful
    """
    try:
        # Update order status to CANCELLED
        async with db.get_connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(queries.CANCEL_EXPIRED_RESERVATION, (order_id,))
                await conn.commit()
        
        # Restore stock in Redis
        redis = redis_client.get_client()
        stock = stock_key(sneaker_id, size)
        await redis.evalsha(
            redis_client.rollback_sha,
            1,
            stock,
            1
        )
        
        logger.info(f"Cancelled order {order_id} and restored stock for sneaker {sneaker_id} size {size}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to cancel order {order_id}: {e}")
        return False


async def run_consistency_check():
    """
    Main consistency check logic
    
    1. Connect to MySQL and Redis
    2. Find expired RESERVED orders
    3. Cancel them and restore stock
    4. Log results
    """
    logger.info("=" * 60)
    logger.info("Starting consistency check...")
    logger.info(f"Timestamp: {datetime.utcnow().isoformat()}")
    
    try:
        # Connect to databases
        await db.connect()
        await redis_client.connect()
        
        # Get expired reservations
        expired = await get_expired_reservations()
        
        if not expired:
            logger.info("No expired reservations found")
            return
        
        logger.info(f"Found {len(expired)} expired reservations")
        
        # Process each expired order
        success_count = 0
        fail_count = 0
        
        for order_id, user_id, sneaker_id, size in expired:
            success = await cancel_order_and_restore_stock(order_id, sneaker_id, size)
            if success:
                success_count += 1
            else:
                fail_count += 1
        
        logger.info(f"Consistency check completed: {success_count} success, {fail_count} failed")
        
    except Exception as e:
        logger.error(f"Consistency check failed: {e}")
        raise
    
    finally:
        # Cleanup
        await db.disconnect()
        await redis_client.disconnect()
        logger.info("Consistency check finished")
        logger.info("=" * 60)


def main():
    """Entry point for CronJob"""
    asyncio.run(run_consistency_check())


if __name__ == "__main__":
    main()