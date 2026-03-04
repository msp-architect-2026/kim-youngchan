"""
Pydantic schemas for product API
Request/Response models with validation
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class SizeStockSchema(BaseModel):
    """Size and stock information schema"""
    size: str
    stock: int
    
    model_config = ConfigDict(from_attributes=True)


class SneakerBaseSchema(BaseModel):
    """Base sneaker schema"""
    brand: str = Field(..., max_length=100, description="Sneaker brand")
    name: str = Field(..., max_length=255, description="Sneaker name")
    price: float = Field(..., gt=0, description="Price in currency")
    drop_at: datetime = Field(..., description="Drop datetime (ISO 8601)")
    
    model_config = ConfigDict(from_attributes=True)


class SneakerCreateSchema(SneakerBaseSchema):
    """Schema for creating a new sneaker with sizes"""
    sizes: List[SizeStockSchema] = Field(
        ...,
        min_length=1,
        description="Available sizes with initial stock"
    )


class SneakerResponseSchema(SneakerBaseSchema):
    """Schema for sneaker response (list view)"""
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SneakerDetailSchema(SneakerResponseSchema):
    """Schema for detailed sneaker view with real-time stock from Redis"""
    sizes: List[SizeStockSchema] = Field(
        default_factory=list,
        description="Sizes with real-time stock from Redis"
    )
    
    model_config = ConfigDict(from_attributes=True)


class SneakerListResponse(BaseModel):
    """Response schema for sneaker list"""
    total: int
    items: List[SneakerResponseSchema]
    cached: bool = Field(
        default=False,
        description="Whether data was served from cache"
    )


class LiveStockResponse(BaseModel):
    """Response schema for live stock check"""
    sneaker_id: int
    total_stock: int
    sizes: List[SizeStockSchema]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    source: str = Field(
        default="redis",
        description="Data source: 'redis' or 'mysql' (fallback)"
    )


class AdminSneakerCreateResponse(BaseModel):
    """Response schema for admin sneaker creation"""
    id: int
    message: str
    cache_warmed: bool = Field(
        default=False,
        description="Whether Redis cache warming was successful"
    )
    
    model_config = ConfigDict(from_attributes=True)


class HealthCheckResponse(BaseModel):
    """Health check response schema"""
    status: str
    database: str
    redis: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str
    error_code: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)