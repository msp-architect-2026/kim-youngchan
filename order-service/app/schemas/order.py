from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatus(str, Enum):
    RESERVED = "RESERVED"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    FAILED = "FAILED"


# ============= Order Endpoints =============

class ReserveRequest(BaseModel):
    user_id: int = Field(..., gt=0, description="User ID")
    sneaker_id: int = Field(..., gt=0, description="Sneaker Product ID")
    size: float = Field(..., ge=220, le=300, description="Shoe size (mm)")


class ReserveResponse(BaseModel):
    success: bool
    message: str
    reserve_token: Optional[str] = None
    expires_in: Optional[int] = None


class ConfirmRequest(BaseModel):
    reserve_token: str = Field(..., min_length=20, max_length=64)


class ConfirmResponse(BaseModel):
    success: bool
    message: str
    order_id: Optional[int] = None


class OrderResponse(BaseModel):
    id: int
    user_id: int
    sneaker_id: int
    size: float
    status: OrderStatus
    reserve_token: str
    created_at: datetime
    updated_at: datetime


class OrderListResponse(BaseModel):
    total: int
    orders: List[OrderResponse]


# ============= Admin Endpoints =============

class KillPodResponse(BaseModel):
    success: bool
    message: str
    pod_name: str
    exit_code: int


class MetricsResponse(BaseModel):
    total_orders: int
    confirmed_orders: int
    reserved_orders: int
    cancelled_orders: int
    failed_orders: int
    success_rate: float


class AdminOrderResponse(BaseModel):
    order_id: int
    user_id: int
    sneaker_id: int
    size: float
    status: OrderStatus
    created_at: datetime