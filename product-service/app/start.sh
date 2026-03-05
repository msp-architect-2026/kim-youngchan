#!/bin/bash
set -e

echo "Starting DropX Product Service..."

# Start metrics server on port 8001 (background)
python3 -c "
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
from app.main import metrics_app

async def run_metrics():
    config = Config()
    config.bind = ['0.0.0.0:8001']
    await serve(metrics_app, config)

asyncio.run(run_metrics())
" &

sleep 2

# Start main app on port 8000 (foreground)
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 1