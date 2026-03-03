#!/bin/bash
# ============================================================
# DropX 누락 이슈 생성 스크립트
# ============================================================

REPO="msp-architect-2026/kim-youngchan"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "================================================"
echo "DropX 신규 이슈 생성"
echo "================================================"
echo ""

echo "Creating: [ Infra ] k3s HTTP Registry 연동 설정 (registries.yaml + imagePullSecret)"
gh issue create --repo "$REPO" \
  --title "[ Infra ] k3s HTTP Registry 연동 설정 (registries.yaml + imagePullSecret)" \
  --body-file "$SCRIPT_DIR/new_issue_1.md"
echo ""

echo "Creating: [ Infra ] Namespace 및 공통 리소스 초기 배포 (ConfigMap/Secret/SA)"
gh issue create --repo "$REPO" \
  --title "[ Infra ] Namespace 및 공통 리소스 초기 배포 (ConfigMap/Secret/SA)" \
  --body-file "$SCRIPT_DIR/new_issue_2.md"
echo ""

echo "Creating: [ Backend ] FastAPI 프로젝트 공통 구조 세팅 (/health, /metrics, pydantic-settings)"
gh issue create --repo "$REPO" \
  --title "[ Backend ] FastAPI 프로젝트 공통 구조 세팅 (/health, /metrics, pydantic-settings)" \
  --body-file "$SCRIPT_DIR/new_issue_3.md"
echo ""

echo "Creating: [ CI/CD ] Dockerfile 작성 및 Registry Push 테스트 (서비스별)"
gh issue create --repo "$REPO" \
  --title "[ CI/CD ] Dockerfile 작성 및 Registry Push 테스트 (서비스별)" \
  --body-file "$SCRIPT_DIR/new_issue_4.md"
echo ""

echo "Creating: [ Infra ] Ingress 리소스 YAML 작성 및 Path 라우팅 배포"
gh issue create --repo "$REPO" \
  --title "[ Infra ] Ingress 리소스 YAML 작성 및 Path 라우팅 배포" \
  --body-file "$SCRIPT_DIR/new_issue_5.md"
echo ""

echo "Creating: [ Backend ] Admin API 구현 (상품 CRUD + 전체 주문 조회 + 시스템 지표)"
gh issue create --repo "$REPO" \
  --title "[ Backend ] Admin API 구현 (상품 CRUD + 전체 주문 조회 + 시스템 지표)" \
  --body-file "$SCRIPT_DIR/new_issue_6.md"
echo ""

echo "Creating: [ LoadTest ] 부하 테스트 결과 종합 분석 보고서"
gh issue create --repo "$REPO" \
  --title "[ LoadTest ] 부하 테스트 결과 종합 분석 보고서" \
  --body-file "$SCRIPT_DIR/new_issue_7.md"
echo ""

echo "✅ 신규 이슈 생성 완료"