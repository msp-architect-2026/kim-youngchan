"""
Prometheus metrics endpoint
Runs on port 8001 (separate from main API port 8000)
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
import time

# Metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

order_reserve_total = Counter(
    'order_reserve_total',
    'Total reserve attempts',
    ['status']  # success, out_of_stock, duplicate, error
)

order_confirm_total = Counter(
    'order_confirm_total',
    'Total confirm attempts',
    ['status']  # success, invalid_token, duplicate, error
)

stock_operations_total = Counter(
    'stock_operations_total',
    'Total stock operations',
    ['operation', 'result']  # reserve/rollback, success/failure
)

active_reservations = Gauge(
    'active_reservations',
    'Number of active reservations (with TTL)'
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics"""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        duration = time.perf_counter() - start_time
        
        # Record metrics
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response


# Metrics app (port 8001)
metrics_app = FastAPI(
    title="Order Service Metrics",
    description="Prometheus metrics endpoint"
)


@metrics_app.get("/metrics")
async def metrics():
    """Prometheus scrape endpoint"""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )


@metrics_app.get("/health")
async def health():
    """Health check for metrics service"""
    return {"status": "healthy"}