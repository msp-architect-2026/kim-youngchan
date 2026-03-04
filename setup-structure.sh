#!/bin/bash
# DropX 프로젝트 디렉토리 구조 생성 스크립트
# 실행 위치: ~/git/team/kim-youngchan
# 실행 방법: bash setup-structure.sh

set -e

BASE_DIR="$(pwd)"
echo "📁 작업 디렉토리: $BASE_DIR"
echo "🚀 DropX 프로젝트 구조 생성 시작..."
echo ""

# ── .gitlab-ci.yml 존재 확인 ──────────────────────────────────
echo "🔍 .gitlab-ci.yml 확인"
if [ -f ".gitlab-ci.yml" ]; then
  echo "   ✅ .gitlab-ci.yml 존재 확인"
else
  echo "   ⚠️  .gitlab-ci.yml 없음 — 루트에 추가 필요"
  touch .gitlab-ci.yml
fi

# ── dropx-chart 존재 확인 (기존 차트 유지) ────────────────────
echo "🔍 dropx-chart/ 확인"
if [ -d "dropx-chart" ]; then
  echo "   ✅ dropx-chart/ 존재 확인 — 기존 차트 유지"
else
  echo "   ⚠️  dropx-chart/ 없음 — Helm 차트를 먼저 추가하세요"
fi

# ── ArgoCD ────────────────────────────────────────────────────
echo ""
echo "🔧 argocd/ 생성"
mkdir -p argocd
[ ! -f argocd/dropx-app.yaml ] && touch argocd/dropx-app.yaml && \
  echo "   → argocd/dropx-app.yaml 생성 (제공된 파일로 교체 필요)"

# ── Database ──────────────────────────────────────────────────
echo ""
echo "🗄️  database/ 생성"
mkdir -p database

# order-service/scripts/ 에서 mv (이동 — 원본 삭제로 단일화)
for f in init.sql init_stock.py; do
  if [ -f "order-service/scripts/$f" ] && [ ! -f "database/$f" ]; then
    echo "   → order-service/scripts/$f → database/$f (이동)"
    mv "order-service/scripts/$f" "database/$f"
  elif [ -f "database/$f" ]; then
    echo "   ✅ database/$f 이미 존재"
  else
    touch "database/$f"
    echo "   → database/$f 빈 파일 생성"
  fi
done

# ── k6 부하 테스트 ─────────────────────────────────────────────
echo ""
echo "🧪 k6/ 생성"
mkdir -p k6

# 기존 load-test.js 있으면 scenario-b 로 이름 변경 후 이동
if [ -f "order-service/tests/load-test.js" ] && [ ! -f "k6/scenario-b-stock-drain.js" ]; then
  echo "   → order-service/tests/load-test.js → k6/scenario-b-stock-drain.js (이동)"
  mv "order-service/tests/load-test.js" "k6/scenario-b-stock-drain.js"
fi
[ ! -f k6/scenario-a-rampup.js ]      && touch k6/scenario-a-rampup.js
[ ! -f k6/scenario-b-stock-drain.js ] && touch k6/scenario-b-stock-drain.js
[ ! -f k6/scenario-c-chaos.js ]       && touch k6/scenario-c-chaos.js

# ── auth-service ──────────────────────────────────────────────
echo ""
echo "🐍 auth-service/ 확인"
mkdir -p auth-service/app/core
mkdir -p auth-service/app/api
mkdir -p auth-service/app/models
[ ! -f auth-service/Dockerfile ]               && touch auth-service/Dockerfile
[ ! -f auth-service/requirements.txt ]         && touch auth-service/requirements.txt
[ ! -f auth-service/app/main.py ]              && touch auth-service/app/main.py
[ ! -f auth-service/app/core/config.py ]       && touch auth-service/app/core/config.py
[ ! -f auth-service/app/core/database.py ]     && touch auth-service/app/core/database.py
[ ! -f auth-service/app/core/security.py ]     && touch auth-service/app/core/security.py
[ ! -f auth-service/app/api/auth.py ]          && touch auth-service/app/api/auth.py
[ ! -f auth-service/app/models/user.py ]       && touch auth-service/app/models/user.py
echo "   ✅ auth-service/ 구조 확인 완료"

# ── product-service ───────────────────────────────────────────
echo ""
echo "🐍 product-service/ 구조 변환 (flat → app/)"
mkdir -p product-service/app

# 루트에 있는 소스파일 → app/ 으로 mv (이동)
for f in main.py database.py models.py service.py; do
  if [ -f "product-service/$f" ] && [ ! -f "product-service/app/$f" ]; then
    echo "   → product-service/$f → product-service/app/$f (이동)"
    mv "product-service/$f" "product-service/app/$f"
  elif [ -f "product-service/app/$f" ]; then
    echo "   ✅ product-service/app/$f 이미 존재"
  else
    touch "product-service/app/$f"
  fi
done
[ ! -f product-service/Dockerfile ]       && touch product-service/Dockerfile
[ ! -f product-service/requirements.txt ] && touch product-service/requirements.txt
echo "   ✅ product-service/ 구조 변환 완료"
echo "   ⚠️  Dockerfile 수정 필요: COPY app/ ./app/ 및 CMD app.main:app 으로 변경"

# ── order-service ─────────────────────────────────────────────
echo ""
echo "🐍 order-service/ 확인"
mkdir -p order-service/app/lua
mkdir -p order-service/app/core
mkdir -p order-service/app/api
mkdir -p order-service/app/db
mkdir -p order-service/app/schemas
mkdir -p order-service/app/jobs

# scripts/*.lua → app/lua/ 로 mv (이동)
for lua in reserve_stock.lua rollback_stock.lua; do
  if [ -f "order-service/scripts/$lua" ] && [ ! -f "order-service/app/lua/$lua" ]; then
    echo "   → order-service/scripts/$lua → order-service/app/lua/$lua (이동)"
    mv "order-service/scripts/$lua" "order-service/app/lua/$lua"
  elif [ -f "order-service/app/lua/$lua" ]; then
    echo "   ✅ order-service/app/lua/$lua 이미 존재"
  else
    touch "order-service/app/lua/$lua"
  fi
done

# scripts/ 폴더가 비었으면 제거
if [ -d "order-service/scripts" ] && [ -z "$(ls -A order-service/scripts)" ]; then
  rmdir "order-service/scripts"
  echo "   → order-service/scripts/ 비어있어 제거"
fi

[ ! -f order-service/Dockerfile ]       && touch order-service/Dockerfile
[ ! -f order-service/requirements.txt ] && touch order-service/requirements.txt
[ ! -f order-service/app/main.py ]      && touch order-service/app/main.py
[ ! -f order-service/app/api/order.py ] && touch order-service/app/api/order.py
[ ! -f order-service/app/api/admin.py ] && touch order-service/app/api/admin.py
[ ! -f order-service/app/jobs/consistency_check.py ] && \
  touch order-service/app/jobs/consistency_check.py
echo "   ✅ order-service/ 구조 확인 완료"
echo "   ⚠️  Dockerfile 수정 필요: scripts/ COPY 줄 제거"

# ── 결과 출력 ─────────────────────────────────────────────────
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ 디렉토리 구조 생성 완료"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 최종 구조:"
find . \
  -not -path './.git/*' \
  -not -path './dropx-chart/*' \
  -not -path './*__pycache__*' \
  -not -path './*.pyc' \
  -not -name '*.pyc' \
  | sort \
  | grep -v "^.$" \
  | sed 's|^\./||' \
  | awk -F/ '{
      depth = NF - 1
      indent = ""
      for (i = 0; i < depth; i++) indent = indent "│   "
      print indent "├── " $NF
    }'

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "⚠️  수동 작업 필요 항목:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  1. argocd/dropx-app.yaml       ← 제공된 파일 내용으로 교체"
echo "  2. product-service/Dockerfile  ← COPY + CMD 경로 수정"
echo "  3. order-service/Dockerfile    ← scripts/ COPY 줄 제거"
echo ""
echo "🎯 완료 후 Git 반영:"
echo "   git add ."
echo "   git commit -m 'refactor: 프로젝트 디렉토리 구조 정리'"
echo "   git push"
echo ""
