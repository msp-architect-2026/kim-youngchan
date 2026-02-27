# [CI/CD] Dockerfile 작성 및 Registry Push 테스트 (서비스별)

## 설명 및 목표
DropX 서비스별 Dockerfile을 작성하고, Private Registry로 이미지 빌드 및 Push 테스트를 수행합니다.

## 작업 내용
- Multi-stage Dockerfile 작성
- 서비스별 이미지 빌드
- GitLab Container Registry에 Push
- imagePullSecret 참조 테스트

## 완료 기준
- 모든 서비스 이미지 Registry에 Push 완료
- Deployment에서 Pull 성공

## 산출물
- Dockerfile (서비스별)
- Registry Push 로그
- imagePullSecret 참조 Deployment YAML
