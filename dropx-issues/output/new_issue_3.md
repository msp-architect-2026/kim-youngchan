# [Backend] FastAPI 프로젝트 공통 구조 세팅 (/health, /metrics, pydantic-settings)

## 설명 및 목표
DropX 백엔드 서비스의 FastAPI 공통 구조를 설정하고, /health, /metrics 엔드포인트 및 Pydantic 기반 설정 skeleton을 구현합니다.

## 작업 내용
- /health, /metrics 엔드포인트 구현
- Pydantic settings 구조 skeleton 생성
- 공통 미들웨어, 예외 처리, 로깅 구조 설정

## 완료 기준
- FastAPI 서버 실행 시 /health, /metrics 응답 확인
- Pydantic settings 정상 로드 확인

## 산출물
- FastAPI 프로젝트 skeleton
- health.py, metrics.py
- settings.py (Pydantic)
