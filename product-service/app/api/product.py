"""
Product API router with business logic
Handles /sneakers endpoints with cache warming and circuit breaker
"""
import json
import logging
from datetime import datetime
from typing import List, Optional, Tuple

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from redis.exceptions import RedisError, ConnectionError, TimeoutError

from app.core.database import get_db
from app.core.redis_client import get_redis, RedisKeyBuilder
from app.core.config import settings
from app.models.sneaker import Sneakers, SneakerSizes
from app.schemas.product import (
    SneakerCreateSchema,
    SneakerResponseSchema,
    SneakerDetailSchema,
    SneakerListResponse,
    LiveStockResponse,
    AdminSneakerCreateResponse,
    SizeStockSchema,
)

logger = logging.getLogger(__name__)

# Router instance
router = APIRouter(prefix="/api", tags=["Product"])


# ============================================================================
# Service Layer (Business Logic)
# ============================================================================

class ProductService:
    """Product service with cache-first strategy and circuit breaker"""
    
    def __init__(self, db_session: AsyncSession, redis_client: Redis):
        self.db = db_session
        self.redis = redis_client
        self._redis_available = True  # Circuit breaker state
    
    async def warm_stock_cache(
        self,
        sneaker_id: int,
        sizes: List[SizeStockSchema]
    ) -> bool:
        """
        Warm Redis cache with initial stock values (CRITICAL for Order Service)
        """
        try:
            pipeline = self.redis.pipeline()
            
            for size_info in sizes:
                key = RedisKeyBuilder.stock_key(sneaker_id, size_info.size)
                pipeline.set(key, size_info.stock)
                logger.info(
                    f"Cache warming: {key} = {size_info.stock}",
                    extra={
                        "sneaker_id": sneaker_id,
                        "size": size_info.size,
                        "stock": size_info.stock
                    }
                )
            
            await pipeline.execute()
            
            logger.info(
                f"Cache warmed successfully for sneaker_id={sneaker_id}",
                extra={"sneaker_id": sneaker_id, "sizes_count": len(sizes)}
            )
            return True
            
        except (RedisError, ConnectionError, TimeoutError) as e:
            logger.error(
                f"Cache warming failed for sneaker_id={sneaker_id}: {e}",
                extra={"sneaker_id": sneaker_id, "error": str(e)}
            )
            self._redis_available = False
            return False
    
    async def get_stock_from_redis(
        self,
        sneaker_id: int
    ) -> Optional[List[SizeStockSchema]]:
        """Fetch stock from Redis for all sizes"""
        if not self._redis_available:
            logger.warning("Redis circuit breaker open")
            return None
        
        try:
            # Get sizes from database
            query = select(SneakerSizes).where(SneakerSizes.sneaker_id == sneaker_id)
            result = await self.db.execute(query)
            db_sizes = result.scalars().all()
            
            if not db_sizes:
                return []
            
            # Fetch stock from Redis using pipeline
            pipeline = self.redis.pipeline()
            for size_record in db_sizes:
                key = RedisKeyBuilder.stock_key(sneaker_id, size_record.size)
                pipeline.get(key)
            
            redis_stocks = await pipeline.execute()
            
            # Combine results
            size_stocks = []
            for size_record, stock_value in zip(db_sizes, redis_stocks):
                stock = int(stock_value) if stock_value is not None else size_record.stock
                size_stocks.append(SizeStockSchema(size=size_record.size, stock=stock))
            
            self._redis_available = True
            return size_stocks
            
        except (RedisError, ConnectionError, TimeoutError) as e:
            logger.error(f"Redis read failed: {e}")
            self._redis_available = False
            return None
    
    async def cache_sneaker_list(
        self,
        sneakers: List[SneakerResponseSchema]
    ) -> bool:
        """Cache sneaker list in Redis"""
        try:
            data = json.dumps([s.model_dump(mode='json') for s in sneakers])
            cache_key = RedisKeyBuilder.sneaker_list_key()
            await self.redis.setex(cache_key, settings.cache_ttl, data)
            logger.info(f"Cached {len(sneakers)} sneakers")
            return True
        except (RedisError, ConnectionError, TimeoutError):
            return False
    
    async def get_cached_sneaker_list(self) -> Optional[List[SneakerResponseSchema]]:
        """Get cached sneaker list from Redis"""
        if not self._redis_available:
            return None
        
        try:
            cache_key = RedisKeyBuilder.sneaker_list_key()
            data = await self.redis.get(cache_key)
            
            if data:
                sneakers_data = json.loads(data)
                logger.info(f"Cache HIT: {len(sneakers_data)} sneakers")
                return [SneakerResponseSchema(**s) for s in sneakers_data]
            
            logger.info("Cache MISS")
            return None
            
        except (RedisError, ConnectionError, TimeoutError):
            self._redis_available = False
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in cache: {e}")
            cache_key = RedisKeyBuilder.sneaker_list_key()
            await self.redis.delete(cache_key)
            return None
    
    async def get_sneaker_list(self) -> SneakerListResponse:
        """Get list of sneakers (cache-first strategy)"""
        # Try cache first
        cached = await self.get_cached_sneaker_list()
        if cached:
            return SneakerListResponse(total=len(cached), items=cached, cached=True)
        
        # Fallback to database
        logger.info("Fetching from database")
        
        now = datetime.utcnow()
        query = select(Sneakers).where(
            or_(
                Sneakers.drop_at > now,
                Sneakers.drop_at <= now
            )
        ).order_by(Sneakers.drop_at.desc())
        
        result = await self.db.execute(query)
        sneakers = result.scalars().all()
        
        items = [SneakerResponseSchema.model_validate(s) for s in sneakers]
        
        if items:
            await self.cache_sneaker_list(items)
        
        return SneakerListResponse(total=len(items), items=items, cached=False)
    
    async def get_sneaker_detail(self, sneaker_id: int) -> Optional[SneakerDetailSchema]:
        """Get detailed sneaker with real-time stock from Redis"""
        query = select(Sneakers).where(Sneakers.id == sneaker_id)
        result = await self.db.execute(query)
        sneaker = result.scalar_one_or_none()
        
        if not sneaker:
            return None
        
        # Get real-time stock
        size_stocks = await self.get_stock_from_redis(sneaker_id)
        
        # Fallback to DB stock
        if size_stocks is None:
            logger.warning(f"Using DB stock for sneaker_id={sneaker_id}")
            size_stocks = [
                SizeStockSchema(size=s.size, stock=s.stock)
                for s in sneaker.sizes
            ]
        
        detail = SneakerDetailSchema.model_validate(sneaker)
        detail.sizes = size_stocks
        return detail
    
    async def get_live_stock(self, sneaker_id: int) -> Optional[LiveStockResponse]:
        """Get real-time stock status"""
        query = select(Sneakers).where(Sneakers.id == sneaker_id)
        result = await self.db.execute(query)
        sneaker = result.scalar_one_or_none()
        
        if not sneaker:
            return None
        
        size_stocks = await self.get_stock_from_redis(sneaker_id)
        source = "redis"
        
        if size_stocks is None:
            logger.warning("Falling back to DB for live stock")
            size_stocks = [
                SizeStockSchema(size=s.size, stock=s.stock)
                for s in sneaker.sizes
            ]
            source = "mysql"
        
        total_stock = sum(s.stock for s in size_stocks)
        
        return LiveStockResponse(
            sneaker_id=sneaker_id,
            total_stock=total_stock,
            sizes=size_stocks,
            source=source
        )
    
    async def create_sneaker(
        self,
        sneaker_data: SneakerCreateSchema
    ) -> Tuple[int, bool]:
        """Create new sneaker and warm cache"""
        sneaker = Sneakers(
            brand=sneaker_data.brand,
            name=sneaker_data.name,
            price=sneaker_data.price,
            drop_at=sneaker_data.drop_at,
        )
        
        self.db.add(sneaker)
        await self.db.flush()
        
        logger.info(f"Created sneaker: id={sneaker.id}, name={sneaker.name}")
        
        # Create sizes
        for size_data in sneaker_data.sizes:
            size_record = SneakerSizes(
                sneaker_id=sneaker.id,
                size=size_data.size,
                stock=size_data.stock,
            )
            self.db.add(size_record)
        
        await self.db.commit()
        await self.db.refresh(sneaker)
        
        # CRITICAL: Warm cache
        cache_warmed = await self.warm_stock_cache(sneaker.id, sneaker_data.sizes)
        
        if not cache_warmed:
            logger.error(
                f"⚠️  CRITICAL: Cache warming FAILED for sneaker_id={sneaker.id}",
                extra={"sneaker_id": sneaker.id, "critical": True}
            )
        
        # Invalidate list cache
        try:
            cache_key = RedisKeyBuilder.sneaker_list_key()
            await self.redis.delete(cache_key)
        except (RedisError, ConnectionError, TimeoutError):
            pass
        
        return sneaker.id, cache_warmed


# ============================================================================
# Dependencies
# ============================================================================

async def get_product_service():
    """Dependency to get ProductService instance"""
    async with get_db() as session:
        redis_client = get_redis()
        yield ProductService(session, redis_client)


# ============================================================================
# API Endpoints
# ============================================================================

@router.get(
    "/sneakers",
    response_model=SneakerListResponse,
    summary="Get sneaker list",
    description="Get list of active and upcoming sneaker drops with cache-first strategy"
)
async def get_sneakers(
    service: ProductService = Depends(get_product_service)
):
    """Get list of sneakers (cache-first)"""
    try:
        return await service.get_sneaker_list()
    except Exception as e:
        logger.error(f"Error fetching sneaker list: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch sneaker list"
        )


@router.get(
    "/sneakers/{sneaker_id}",
    response_model=SneakerDetailSchema,
    summary="Get sneaker detail",
    description="Get detailed sneaker information with real-time stock from Redis"
)
async def get_sneaker_detail(
    sneaker_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Get detailed sneaker with real-time stock"""
    try:
        sneaker = await service.get_sneaker_detail(sneaker_id)
        
        if not sneaker:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sneaker not found: {sneaker_id}"
            )
        
        return sneaker
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching sneaker detail: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch sneaker detail"
        )


@router.get(
    "/sneakers/{sneaker_id}/stock/live",
    response_model=LiveStockResponse,
    summary="Get live stock",
    description="Get real-time stock status (Redis-only for maximum speed)"
)
async def get_live_stock(
    sneaker_id: int,
    service: ProductService = Depends(get_product_service)
):
    """Get real-time stock status"""
    try:
        stock_info = await service.get_live_stock(sneaker_id)
        
        if not stock_info:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sneaker not found: {sneaker_id}"
            )
        
        return stock_info
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching live stock: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch live stock"
        )


@router.post(
    "/admin/sneakers",
    response_model=AdminSneakerCreateResponse,
    summary="Create sneaker product",
    description="Create new sneaker and warm cache (critical for Order Service)",
    status_code=status.HTTP_201_CREATED
)
async def create_sneaker(
    sneaker_data: SneakerCreateSchema,
    service: ProductService = Depends(get_product_service)
):
    """Create new sneaker product and warm cache"""
    try:
        sneaker_id, cache_warmed = await service.create_sneaker(sneaker_data)
        
        if cache_warmed:
            logger.info(f"✅ Sneaker created with cache warming: {sneaker_data.name}")
        else:
            logger.error(f"⚠️  Sneaker created but cache warming FAILED")
        
        return AdminSneakerCreateResponse(
            id=sneaker_id,
            message=f"Sneaker created successfully: {sneaker_data.name}",
            cache_warmed=cache_warmed
        )
    except Exception as e:
        logger.error(f"Error creating sneaker: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create sneaker"
        )