from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import get_settings
from app.core.database import db
from app.core.redis_client import redis_client
from app.api import order, admin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifecycle management
    
    Startup:
    - Connect to MySQL
    - Connect to Redis
    - Load Lua scripts
    
    Shutdown:
    - Close all connections
    """
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    
    try:
        await db.connect()
        logger.info("✓ MySQL connected")
        
        await redis_client.connect()
        logger.info("✓ Redis connected")
        logger.info("✓ Lua scripts loaded")
        
        logger.info("Application ready to serve requests")
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    await db.disconnect()
    await redis_client.disconnect()
    logger.info("Application stopped")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="DropX Order Service - Atomic stock management with Redis Lua + MySQL",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(order.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health():
    db_ok = db.pool is not None
    redis_ok = redis_client.client is not None
    
    if not db_ok or not redis_ok:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "db": db_ok, "redis": redis_ok}
        )
    
    return {"status": "healthy", "db": True, "redis": True}


@app.get("/live")
async def liveness():
    """Kubernetes liveness probe"""
    return {"status": "alive"}


@app.get("/ready")
async def readiness():
    """Kubernetes readiness probe"""
    # Could add database connectivity checks here
    return {"status": "ready"}