from __future__ import annotations

import asyncio
import time
from contextlib import asynccontextmanager

import aiomysql
import redis.asyncio as aioredis
import uvicorn
from fastapi import FastAPI, Request, Response, status
from prometheus_client import (
    CollectorRegistry,
    Counter,
    Histogram,
    make_asgi_app,
)

from app.api.auth import router as auth_router
from app.core.config import get_settings
from app.core.database import get_mysql_pool, get_redis_client, shutdown, startup

settings = get_settings()

# ---------------------------------------------------------------------------
# Prometheus  (isolated registry)
# ---------------------------------------------------------------------------

REGISTRY = CollectorRegistry(auto_describe=True)

http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status_code"],
    registry=REGISTRY,
)

http_request_duration_seconds = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.2, 0.5, 1.0, 2.5),
    registry=REGISTRY,
)

metrics_app = make_asgi_app(registry=REGISTRY)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup(app)
    metrics_task = asyncio.create_task(_serve_metrics())
    yield
    metrics_task.cancel()
    await shutdown(app)


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------

app = FastAPI(
    title="DropX Auth Service",
    version="1.0.0",
    docs_url="/docs" if settings.app_env != "production" else None,
    redoc_url=None,
    lifespan=lifespan,
)


# ---------------------------------------------------------------------------
# Prometheus middleware
# ---------------------------------------------------------------------------

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status_code=str(response.status_code),
    ).inc()
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path,
    ).observe(duration)

    return response


# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

app.include_router(auth_router)


# ---------------------------------------------------------------------------
# Health  (K8s liveness / readiness)
# ---------------------------------------------------------------------------

@app.get("/health/live", status_code=status.HTTP_200_OK, tags=["ops"])
async def liveness() -> dict:
    return {"status": "alive"}


@app.get("/health/ready", status_code=status.HTTP_200_OK, tags=["ops"])
async def readiness() -> dict:
    errors: list[str] = []

    try:
        pool: aiomysql.Pool = get_mysql_pool()
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT 1")
    except Exception as exc:
        errors.append(f"mysql: {exc}")

    try:
        r: aioredis.Redis = get_redis_client()
        await r.ping()
    except Exception as exc:
        errors.append(f"redis: {exc}")

    if errors:
        return Response(
            content=str({"status": "degraded", "errors": errors}),
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            media_type="application/json",
        )

    return {"status": "ready"}


# ---------------------------------------------------------------------------
# Metrics server  (port 8001, make_asgi_app)
# ---------------------------------------------------------------------------

async def _serve_metrics() -> None:
    config = uvicorn.Config(
        app=metrics_app,
        host="0.0.0.0",
        port=settings.metrics_port,
        loop="none",
        log_level="warning",
        access_log=False,
    )
    server = uvicorn.Server(config)
    await server.serve()