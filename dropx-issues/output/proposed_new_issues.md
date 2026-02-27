# DropX 로드맵 누락 이슈 제안

기존 이슈 분석 결과, 아래 작업들이 로드맵에 빠져 있어 추가를 제안합니다.

---

## 🆕 제안 #1: [ Infra ] k3s HTTP Registry 연동 설정

> **근거**: PC #2 GitLab Registry(HTTP)를 k3s에서 pull 하려면 `registries.yaml` + `imagePullSecret`이 필수. 현재 이를 다루는 이슈 없음.

### 설명
k3s에서 PC #2 GitLab Container Registry(HTTP, 비TLS)의 이미지를 pull 할 수 있도록 registries.yaml 및 imagePullSecret을 설정합니다.

### 작업 내용
- [ ] `/etc/rancher/k3s/registries.yaml` 작성 (insecure registry 등록)
- [ ] k3s 서비스 재시작 (`systemctl restart k3s`)
- [ ] `dropx` namespace에 `imagePullSecret` 생성 (docker-registry 타입)
- [ ] Deployment에 `imagePullSecrets` 필드 추가 확인

### 완료 기준
- [ ] `crictl pull 192.168.10.100:5050/root/ci/...` 이미지 pull 성공
- [ ] Pod 생성 시 ImagePullBackOff 없이 정상 기동

### 산출물
- `/etc/rancher/k3s/registries.yaml` 설정 파일
- `kubectl get secret` imagePullSecret 확인 스크린샷

---

## 🆕 제안 #2: [ Infra ] Namespace 및 공통 리소스 초기 배포

> **근거**: `dropx` namespace, ConfigMap, Secret(실값) 생성이 모든 서비스 배포의 선행 작업인데 전용 이슈 없음.

### 설명
`dropx` namespace를 생성하고, 모든 서비스가 공유하는 ConfigMap과 Secret(실값)을 배포합니다.

### 작업 내용
- [ ] `dropx` namespace 생성
- [ ] ConfigMap 배포 (DB 호스트, Redis 호스트, 앱 공통 설정)
- [ ] Secret 실값 입력: MySQL Root PW, JWT_SECRET_KEY, Registry Token
- [ ] `dropx-app-sa` ServiceAccount 생성

### 완료 기준
- [ ] `kubectl get ns dropx` 정상
- [ ] `kubectl get configmap,secret -n dropx` 모든 리소스 존재 확인

### 산출물
- `namespace.yaml`, `configmap.yaml`, `secret.yaml` 매니페스트
- `kubectl get all -n dropx` 출력 스크린샷

---

## 🆕 제안 #3: [ Backend ] FastAPI 프로젝트 공통 구조 세팅

> **근거**: 3개 서비스(auth/product/order)의 공통 프로젝트 skeleton 세팅이 별도 이슈로 없음. pydantic-settings, 비동기 DB 풀, /health, /metrics 엔드포인트 등 공통 기반.

### 설명
auth-service, product-service, order-service 3개 FastAPI 프로젝트의 공통 구조(skeleton)를 세팅합니다.

### 작업 내용
- [ ] 프로젝트 디렉토리 구조 정의 (`app/`, `app/routes/`, `app/core/`, `app/schemas/`)
- [ ] `pydantic-settings` 기반 환경변수 관리 (`app/core/config.py`)
- [ ] aiomysql 커넥션 풀 유틸리티 (`app/core/database.py`)
- [ ] redis.asyncio 클라이언트 초기화 (`app/core/redis.py`)
- [ ] `/health` Liveness/Readiness probe 엔드포인트
- [ ] `/metrics` (port 8001) Prometheus 메트릭 엔드포인트 (prometheus-fastapi-instrumentator)
- [ ] `requirements.txt` 의존성 정의

### 완료 기준
- [ ] 3개 서비스 모두 `uvicorn` 기동 시 `/health` 200 OK 응답
- [ ] `/metrics` 엔드포인트에서 Prometheus 형식 메트릭 출력

### 산출물
- 3개 서비스 프로젝트 디렉토리 구조 (`tree` 출력)
- `requirements.txt`
- `/health`, `/metrics` 응답 스크린샷

---

## 🆕 제안 #4: [ CI/CD ] Dockerfile 작성 (서비스별)

> **근거**: 3개 서비스의 Docker 이미지 빌드를 위한 Dockerfile이 별도 이슈로 없음.

### 설명
auth-service, product-service, order-service 각각의 Dockerfile을 작성하고 로컬 빌드 테스트를 수행합니다.

### 작업 내용
- [ ] Multi-stage build Dockerfile 작성 (Python slim 기반)
- [ ] `.dockerignore` 작성
- [ ] 로컬 `docker build` 및 `docker run` 테스트
- [ ] GitLab Registry(192.168.10.100)에 수동 push 테스트

### 완료 기준
- [ ] 3개 서비스 Docker 이미지 빌드 성공
- [ ] 컨테이너 실행 후 `/health` 응답 확인
- [ ] GitLab Registry에 push 성공

### 산출물
- `auth-service/Dockerfile`
- `product-service/Dockerfile`
- `order-service/Dockerfile`
- `docker images` 목록 스크린샷
- GitLab Registry 이미지 목록 스크린샷

---

## 🆕 제안 #5: [ Infra ] Ingress 리소스 YAML 작성 및 배포

> **근거**: #3(Ingress Controller 설치)와 #28은 있지만, 실제 DropX path-based routing Ingress 리소스(YAML) 작성 이슈가 별도로 없음.

### 설명
`dropx.local` 호스트로 들어오는 요청을 auth-service, product-service, order-service로 라우팅하는 Ingress 리소스를 작성·배포합니다.

### 작업 내용
- [ ] `dropx.local` 호스트 기반 Ingress YAML 작성
- [ ] Path 매핑: `/api/signup`, `/api/login`, `/api/me` → auth-service
- [ ] Path 매핑: `/api/sneakers/*` → product-service
- [ ] Path 매핑: `/api/orders/*`, `/api/admin/*` → order-service
- [ ] PC #2 `/etc/hosts`에 `192.168.10.230 dropx.local` 등록

### 완료 기준
- [ ] `curl http://dropx.local/api/sneakers` 정상 응답
- [ ] 각 Path가 올바른 서비스로 라우팅됨 확인

### 산출물
- `ingress-dropx.yaml` 매니페스트
- `kubectl describe ingress` 출력
- Path별 curl 테스트 결과 스크린샷

---

## 🆕 제안 #6: [ Backend ] Admin API 구현 (상품 등록/삭제 + 전체 주문 조회)

> **근거**: API 명세에 `POST /admin/sneakers`, `DELETE /admin/sneakers/{id}`, `GET /admin/orders` 등 Admin API가 정의되어 있지만 전용 구현 이슈가 없음.

### 설명
관리자 전용 API(상품 등록, 상품 삭제, 전체 주문 조회, 시스템 지표 요약)를 구현합니다.

### 작업 내용
- [ ] `POST /api/admin/sneakers` 상품 등록 (ADMIN role 검증)
- [ ] `DELETE /api/admin/sneakers/{id}` 상품 삭제
- [ ] `GET /api/admin/orders` 전체 주문 조회
- [ ] `GET /api/admin/metrics` 시스템 지표 요약 (Redis 통계 + HPA 상태)
- [ ] MySQL sneakers + sneaker_sizes INSERT 시 Redis `stock:{id}:{size}` 자동 초기화

### 완료 기준
- [ ] ADMIN role JWT로만 접근 가능 (USER role → 403)
- [ ] 상품 등록 시 MySQL + Redis 동시 초기화 확인

### 산출물
- `product-service/app/routes/admin.py` 소스코드
- `order-service/app/routes/admin.py` 소스코드
- Admin API 테스트 결과 스크린샷

---

## 🆕 제안 #7: [ LoadTest ] 부하 테스트 결과 분석 보고서 작성

> **근거**: 테스트 실행 이슈(#69, #70)는 있지만, 결과를 정리하여 면접용 분석 보고서로 만드는 이슈가 없음.

### 설명
k6 부하 테스트 및 Kill-Pod 장애 주입 테스트 결과를 종합 분석하여 면접 데모용 성능 리포트를 작성합니다.

### 작업 내용
- [ ] 5,000 VU 스파이크 테스트 결과 정리 (TPS, p95, 에러율)
- [ ] Kill-Pod 장애 주입 시 복구 시간 및 성공률 영향 분석
- [ ] HPA Scale-out 시점 vs CPU 사용률 상관관계 분석
- [ ] 재고 정합성 최종 검증 (Redis stock + MySQL orders = 초기 재고)
- [ ] 병목 지점 식별 및 개선 방안 제시

### 완료 기준
- [ ] 모든 KPI 달성 여부 명확히 기록 (p95 ≤ 200ms, 재고 음수 0건)
- [ ] 면접 시 30초 내 핵심 수치 설명 가능

### 산출물
- 성능 테스트 분석 보고서 (Markdown 또는 PDF)
- 주요 그래프/차트 이미지 (Grafana Export)
- Wiki 06-Performance-Test 페이지 최종 업데이트
