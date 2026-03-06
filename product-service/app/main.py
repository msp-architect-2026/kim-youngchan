"""
FastAPI Main Application for Product Service
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, Gauge, make_asgi_app, REGISTRY

from app.core.config import settings
from app.core.database import init_db, close_db, check_db_health
from app.core.redis_client import init_redis, close_redis, check_redis_health
from app.api.product import router as product_router
from app.schemas.product import HealthCheckResponse, ErrorResponse

# ============================================================================
# Logging Configuration
# ============================================================================

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='{"timestamp":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
    datefmt='%Y-%m-%dT%H:%M:%S'
)

logger = logging.getLogger(__name__)

# ============================================================================
# Prometheus Metrics
# ============================================================================

REQUEST_COUNT = Counter(
    'product_service_requests_total',
    'Total request count',
    ['method', 'endpoint', 'status'],
    registry=REGISTRY
)

REQUEST_DURATION = Histogram(
    'product_service_request_duration_seconds',
    'Request duration in seconds',
    ['method', 'endpoint'],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0),
    registry=REGISTRY
)

CACHE_HITS = Counter(
    'product_service_cache_hits_total',
    'Total cache hits',
    ['cache_type'],
    registry=REGISTRY
)

CACHE_MISSES = Counter(
    'product_service_cache_misses_total',
    'Total cache misses',
    ['cache_type'],
    registry=REGISTRY
)

REDIS_ERRORS = Counter(
    'product_service_redis_errors_total',
    'Total Redis errors',
    registry=REGISTRY
)

CACHE_WARMING_SUCCESS = Counter(
    'product_service_cache_warming_success_total',
    'Total successful cache warming operations',
    registry=REGISTRY
)

CACHE_WARMING_FAILURE = Counter(
    'product_service_cache_warming_failure_total',
    'Total failed cache warming operations',
    registry=REGISTRY
)

ACTIVE_REQUESTS = Gauge(
    'product_service_active_requests',
    'Number of active requests',
    registry=REGISTRY
)

# ============================================================================
# Application Lifecycle
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    logger.info("=" * 60)
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info("=" * 60)
    
    logger.info("Configuration:")
    logger.info(f"  Database: {settings.db_host}:{settings.db_port}/{settings.db_name}")
    logger.info(f"  DB Pool: pool_size={settings.db_pool_size}, max_overflow={settings.db_max_overflow}")
    logger.info(f"  Redis: {settings.redis_host}:{settings.redis_port}/{settings.redis_db}")
    logger.info(f"  Redis Pool: max_connections={settings.redis_max_connections}")
    
    try:
        await init_db()
        await init_redis()
        logger.info("✅ All connections initialized successfully")
    except Exception as e:
        logger.error(f"❌ Failed to initialize connections: {e}")
        raise
    
    logger.info("=" * 60)
    logger.info(f"{settings.app_name} is ready")
    logger.info("=" * 60)
    
    yield
    
    logger.info("Shutting down...")
    await close_db()
    await close_redis()
    logger.info("✅ Shutdown complete")

# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title=settings.app_name,
    description="High-performance product and stock management service",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    debug=settings.debug
)

# ============================================================================
# Middleware
# ============================================================================

@app.middleware("http")
async def metrics_middleware(request, call_next):
    """Middleware to track request metrics"""
    method = request.method
    path = request.url.path
    
    ACTIVE_REQUESTS.inc()
    
    try:
        with REQUEST_DURATION.labels(method=method, endpoint=path).time():
            response = await call_next(request)
        
        REQUEST_COUNT.labels(
            method=method,
            endpoint=path,
            status=response.status_code
        ).inc()
        
        return response
    finally:
        ACTIVE_REQUESTS.dec()

# ============================================================================
# Include Routers
# ============================================================================

app.include_router(product_router)

# ============================================================================
# Endpoints
# ============================================================================

@app.get(
    "/health",
    response_model=HealthCheckResponse,
    tags=["Monitoring"]
)
async def health_check():
    """Health check endpoint for Kubernetes probes"""
    db_healthy = await check_db_health()
    redis_healthy = await check_redis_health()
    
    overall_healthy = db_healthy and redis_healthy
    status_code = status.HTTP_200_OK if overall_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
    
    return JSONResponse(
        status_code=status_code,
        content=HealthCheckResponse(
            status="healthy" if overall_healthy else "degraded",
            database="ok" if db_healthy else "error",
            redis="ok" if redis_healthy else "error"
        ).model_dump(mode="json")
    )

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "running"
    }

# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """General exception handler"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ErrorResponse(
            detail="Internal server error",
            error_code="INTERNAL_ERROR"
        ).model_dump()
    )

# ============================================================================
# Metrics App for Port 8001 (used by start.sh)
# ============================================================================

metrics_app = make_asgi_app(registry=REGISTRY)  # ⚠️ 이 한 줄만 추가!