# ── 1단계: 패키지 설치 ────────────────────────────────────────
FROM python:3.12-slim AS deps

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── 2단계: 최소 런타임 이미지 ────────────────────────────────
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# deps 단계 패키지만 복사 (빌드 잔재 제외)
COPY --from=deps /install /usr/local

COPY app/ ./app/

EXPOSE 8000 8001

# K8s HPA 수평 확장 전제 → workers=1 유지
# uvloop + httptools 조합으로 단일 워커 성능 최대화
CMD ["uvicorn", "app.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "1", \
     "--loop", "uvloop", \
     "--http", "httptools", \
     "--no-access-log"]
