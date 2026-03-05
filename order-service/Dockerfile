FROM python:3.11-slim

WORKDIR /app

# 필수 빌드 도구만 설치 (curl 제거)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

# 보안을 위한 비루트 사용자 설정
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# 서비스용 8000, 메트릭용 8001
EXPOSE 8000 8001

# Docker HEALTHCHECK는 삭제합니다. (K8s Probe가 대신 수행)

# Run main app on 8000 and metrics on 8001
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 & \
    uvicorn app.metrics:metrics_app --host 0.0.0.0 --port 8001 --workers 1 && \
    wait