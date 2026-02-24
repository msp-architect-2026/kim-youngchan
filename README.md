# 🚀 DropX

> **"대량의 동시 접속자가 100개의 한정판 상품을 구매하는 순간, 재고의 음수 없이 데이터 정합성을 보장하는 Kubernetes 기반 GitOps 주문 인프라 플랫폼"**

본 시스템은 한정판 재고 판매 시나리오를 기반으로 **Redis Atomic 연산**을 통해 재고 정합성을 보장하고, **Kubernetes HPA 및 Pod 장애 상황**에서도 서비스 가용성과 성공률을 유지하는 것을 목표로 합니다.

---

## 1️⃣ Why DropX Exists (기획 배경)
한정판 상품 드롭(Drop) 상황에서는 일반적인 쇼핑몰 아키텍처로 감당할 수 없는 다음 문제들이 발생합니다:
*  **순간 트래픽 폭증 (Spike Traffic)**
*  **DB Lock 경합 및 커넥션 풀 고갈**
*  **재고 음수 발생 (Race Condition)**
*  **Pod 과부하 및 연쇄 장애**
*  **배포 중 서비스 중단**

DropX는 단순한 기능 구현을 넘어, **위의 인프라/동시성 문제들을 아키텍처 관점에서 어떻게 해결하는지 증명**하기 위해 설계되었습니다.

---

## 2️⃣ Core Problem & Goals (목표 지표)
* **동시 접속자:** 5,000 VU (Virtual Users)
* **한정판 재고:** 100개
* **재고 음수:** **0건**
* **평균 응답속도:** 200ms 이하 보장
* **장애 대응:** Pod 강제 종료 시 자동 복구 및 성공률 유지

---

## 3️⃣ 핵심 해결 전략 (Core Strategies)

### 3-1. 재고 정합성 보장 (Data Integrity)
* **문제:** 동시에 5,000명이 `UPDATE stock = stock - 1`을 요청하면 Race Condition이 발생하여 재고가 음수가 됨.
* **해결 방식: Redis Atomic 연산 + Lua Script**
  1. Redis에서 재고 `DECR` (원자적 처리)
  2. 성공(0 이상)한 요청만 MySQL Insert (비동기/배치)
  3. 실패(음수)한 요청은 즉시 품절 반환 및 `INCR` 복구
  * **효과:** DB Lock 최소화, 초저지연 처리, 재고 음수 0 보장.



### 3-2. 트래픽 폭증 대응 (Auto Scaling)
* **Kubernetes HPA (Horizontal Pod Autoscaler)** 적용
* CPU 사용률 60% 초과 시 `Order Service` Pod을 1개에서 최대 5개로 자동 Scale-out.

### 3-3. 장애 대응 (Self-Healing)
* 관리자 API를 통한 **Pod 강제 종료(Kill Pod)** 테스트 환경 구축.
* `StatefulSet` 기반 DB/Redis 영속성 복구.
* `ReplicaSet` 기반 서비스 자동 복구 및 트래픽 재조정.

### 3-4. GitOps 기반 배포 자동화
```text
Git Push → GitLab CI(Build) → Helm Update → ArgoCD Sync → K8s Rollout
```
* Git이 인프라의 Source of Truth 역할을 수행.
* 완벽한 Rollback 실습 및 선언적 배포 구현.

---

## 4️⃣ System Architecture

아래는 본 프로젝트의 전체 시스템 구조도입니다.

<img width="2112" height="1578" alt="최종 아키텍처 이미지 drawio" src="https://github.com/user-attachments/assets/14ac94c6-6bba-46db-bf5b-a09dadf1bd0e" />

---

## 5️⃣ Tech Stack & Why

### 인프라 및 모니터링
* **Kubernetes (Bare-Metal):** MSA 운영 최적화, Self-Healing, HPA 자동 확장 (VM 3대 클러스터링)
* **MetalLB + Nginx Ingress:** 베어메탈 환경의 L4/L7 라우팅 및 TLS 시뮬레이션
* **GitLab CI + ArgoCD:** 선언적 배포(GitOps), Sync History 관리
* **Helm Chart:** 환경별(Dev/Prod) `values.yaml` 관리
* **Observability (PLG Stack):** Prometheus(메트릭), Grafana(대시보드), Alertmanager

### 개발 스택 선택 이유

| Component | 선택 기술 | 선택 이유 (Why Not Java/Spring?) |
| :--- | :--- | :--- |
| **Backend** | **Python (FastAPI)** | JVM 대비 컨테이너 초기 구동(Cold Start) 시간이 짧아 HPA 확장에 유리함. 비동기(Async) 처리와 Redis Lua Script 연동이 매우 간결함. |
| **Frontend** | **React** | SPA 기반 사용자 구매 UI 및 WebSocket을 통한 실시간 지표 렌더링. |
| **Database** | **MySQL 8.0** | 트랜잭션 지원, 정규화 기반 주문 데이터 영속성 보장 (StatefulSet). |
| **Cache** | **Redis** | 메모리 기반 고속 처리, 원자적 재고 관리 (StatefulSet). |

---

##  6️⃣ API 명세서 (v1.0 Draft)

**Base URL:** `/api`

###  6-1. 인증 (Auth)

| Method | Endpoint | Description | Request Body | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/signup` | 회원가입 | `{"email": "...", "password": "...", "name": "..."}` | `{"message": "회원가입이 완료되었습니다."}` |
| `POST` | `/login` | 로그인 | `{"email": "...", "password": "..."}` | `{"accessToken": "...", "userId": 1, "name": "..."}` |
| `GET` | `/me` | 내 정보 조회 | `Header: Authorization: Bearer {token}` | `{"id": 1, "email": "...", "name": "..."}` |

###  6-2. 상품 (Product)

| Method | Endpoint | Description | Request Body | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/products` | 상품 목록 조회 | `-` | `[{"id": 1, "name": "한정판 운동화", "price": 150000, "stock": 100}]` |
| `GET` | `/products/{id}` | 상품 상세 조회 | `-` | `{"id": 1, "name": "...", "price": 150000, "stock": 100}` |
| `POST` | `/admin/products` | 상품 등록 (관리자) | `{"name": "...", "price": 150000, "stock": 100}` | `{"message": "상품 등록 완료"}` |
| `PUT` | `/admin/products/{id}` | 상품 수정 (관리자) | `{"price": 160000, "stock": 120}` | `{"message": "상품 수정 완료"}` |

###  6-3. 재고 선점

> **Redis 기반 원자적 감소 처리 및 동시성 제어 핵심 구간**

| Method | Endpoint | Description | Request Body | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/orders/reserve` | 재고 선점 요청 | `{"productId": 1}` | `{"success": true, "message": "선점 성공"}` |
| `POST` | `/orders/confirm` | 주문 확정 | `{"productId": 1}` | `{"orderId": 101, "status": "CONFIRMED"}` |
| `POST` | `/orders/cancel` | 선점 취소 | `{"productId": 1}` | `{"message": "선점 취소 완료"}` |

#### 선점 실패 시 응답
```json
{
  "success": false,
  "message": "재고가 부족합니다."
}
```

###  6-4. 주문 (Order)

| Method | Endpoint | Description | Request | Response (Success) |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/orders` | 내 주문 목록 조회 | `Header: Authorization` | `[{"orderId": 101, "productId": 1, "status": "CONFIRMED"}]` |
| `GET` | `/orders/{orderId}` | 주문 상세 조회 | `-` | `{"orderId": 101, "productId": 1, "status": "CONFIRMED"}` |


###  6-5. 관리자 영역 (Infra + 운영 시뮬레이션)

| Method | Endpoint | Description | Request Body | Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/admin/kill-pod` | Pod 강제 종료 시뮬레이션 | `{"podName": "app-1234"}` | `{"message": "Pod 종료 요청 완료"}` |
| `GET` | `/admin/metrics` | 시스템 지표 요약 조회 | `-` | `{"activeUsers": 3000, "successRate": 92.1}` |
| `GET` | `/admin/orders` | 전체 주문 조회 | `-` | `[{"orderId": 101, "status": "CONFIRMED"}]` |


### 🛡️ 인증 / 권한 정책
* **일반 API:** 로그인 사용자 전용 (`Bearer Token` 필요)
* **`/api/admin/*`:** `ADMIN` Role 권한 필요
* **`kill-pod` API:** Kubernetes RBAC 연동 및 인프라 관리자 권한 필수

---

## 7️⃣ Observability Stack (관측성)
단순한 로그 확인을 넘어 시스템의 수치(Metric)를 시각화하여 모니터링합니다.

* **Prometheus:** 실시간 RPS, 응답 시간(p95), Pod 상태 메트릭 수집
* **Grafana:** 수집된 메트릭을 바탕으로 'DropX 통합 대시보드' 구축
* **Loki:** 분산 환경의 로그를 중앙에서 통합 검색 및 분석
* **Alertmanager:** 임계치 초과(예: 재고 0, Pod Restart) 시 Slack 실시간 알림

---

##  8️⃣ Kubernetes Workload 설계

| 리소스 타입 | 대상 컴포넌트 | 설계 의도 |
| :--- | :--- | :--- |
| **Deployment** | Auth, Product, Order | Stateless 앱의 수평 확장(HPA) 지원 |
| **StatefulSet** | MySQL, Redis | 데이터의 연속성과 고유 식별자 유지 (PVC 연동) |
| **HPA** | Order Service | CPU/Memory 사용량에 따른 동적 Pod 확장 |
| **ConfigMap** | 공통 설정 값 | 코드와 설정의 분리 (Environment Variables) |
| **Secret** | DB, JWT Secret | 데이터베이스 접속 정보 및 인증 키 등 민감 정보 암호화 |
| **CronJob** | 정기 배치 작업 | 일회성 데이터 정합성 검증 및 로그 정리 |

---

## 9️⃣ 데이터 모델링 (MySQL + Redis)

> DropX는 대규모 트래픽 환경에서 한정판 상품(Drop)을 안정적으로 판매하기 위해 **영구 저장소(MySQL)**와 **고속 정합성 레이어(Redis)**를 분리하여 설계되었습니다.

###  MySQL: 관계형 데이터베이스 (Persistence Layer)

#### 📌 Table 1: `users` (사용자)
| 컬럼명 | 타입 | 제약조건 | 설명 |
| :--- | :--- | :--- | :--- |
| **id** | BIGINT | PK, AI | 고유 사용자 ID |
| **email** | VARCHAR(100) | UNIQUE, NOT NULL | 로그인 이메일 |
| **password_hash** | VARCHAR(255) | NOT NULL | 암호화된 비밀번호 |
| **role** | ENUM | DEFAULT 'USER' | 권한 (`USER`, `ADMIN`) |
| **is_deleted** | BOOLEAN | DEFAULT FALSE | 소프트 삭제 여부 |
| **created_at** | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | 가입 일시 |

#### 📌 Table 2: `products` (상품)
| 컬럼명 | 타입 | 제약조건 | 설명 |
| :--- | :--- | :--- | :--- |
| **id** | BIGINT | PK, AI | 상품 고유 ID |
| **name** | VARCHAR(100) | NOT NULL | 상품명 |
| **price** | DECIMAL(12,2) | NOT NULL | 상품 가격 |
| **total_stock** | INT | NOT NULL | 초기 전체 재고 |
| **is_drop** | BOOLEAN | DEFAULT FALSE | 드롭 상품 여부 |
| **drop_start_at** | DATETIME | NULL | 판매 시작 시간 |
| **drop_end_at** | DATETIME | NULL | 판매 종료 시간 |

#### 📌 Table 3: `orders` (주문)
| 컬럼명 | 타입 | 제약조건 | 설명 |
| :--- | :--- | :--- | :--- |
| **id** | BIGINT | PK, AI | 주문 고유 번호 |
| **user_id** | BIGINT | FK (users.id) | 주문자 ID |
| **product_id** | BIGINT | FK (products.id) | 주문 상품 ID |
| **status** | ENUM | NOT NULL | 상태 (`SUCCESS`, `CANCEL`) |
| **process_ms** | INT | NULL | 처리 소요 시간(ms) |

> **인덱스 전략** > `UNIQUE KEY uk_user_product (user_id, product_id)` : 1인 1개 구매 제한 방어

---

###  Redis: 인메모리 데이터 (Speed Layer)

| 기능 분류 | Key 패턴 | Type | 설명 |
| :--- | :--- | :--- | :--- |
| **실시간 재고** | `stock:product:{id}` | String | Lua Script 기반 원자적 차감 |
| **중복 방지** | `order:lock:{pId}:{uId}` | String | SETNX 기반 락 (TTL 5분) |
| **실시간 지표** | `metrics:drop:{status}` | String | 성공/실패 INCR 통계 수집 |

---

###  주문 처리 시나리오 (Order Process)

1. **중복 체크**: `SETNX order:lock:{pId}:{uId}` 성공 시 진행
2. **재고 차감**: Lua Script를 통한 원자적 수량 체크 및 `DECR`
   ```lua
   local stock = tonumber(redis.call("get", KEYS[1]) or "0")
   if stock > 0 then redis.call("decr", KEYS[1]) return 1 else return 0 end

---

## 🔟 결론
DropX는 단순 이커머스가 아니다
동시성 충돌 상황에서 재고 정합성을 보장하는 실무형 kubernetes GitOps 기반 운영 시스템이다.
