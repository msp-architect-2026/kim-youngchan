<img width="2112" height="1578" alt="최종 아키텍처 이미지 drawio" src="https://github.com/user-attachments/assets/1016ce28-8b60-463c-a2e5-135b2d131507" /># 🛒 DropX — 대규모 선착순 한정판 주문 시스템 (High-Concurrency Order System)

> **5,000 동시 접속 환경에서도 재고 정합성을 보장하는 Kubernetes 기반 MSA 주문 시스템**

---

# 📌 1. 프로젝트 개요 (Overview)

DropX는 한정판 상품 판매 시 발생하는 **Spike Traffic (동시 접속 폭증)** 상황을 가정하여,

- 자동 확장 (Auto Scaling)
- 트래픽 분산 (Load Balancing)
- 선언형 배포 (GitOps)
- 인프라 복원력 (Resilience)
- 실시간 관측 (Observability)
- 재고 음수 방지 (Data Consistency)

5,000명의 동시 접속자(Spike Traffic)가 몰리는 선착순 한정판 상품 판매 환경에서, 병목 현상을 방지하고 데이터 정합성(재고 0 이하 방지)을 보장하는 MSA 기반의 주문/결제 시스템입니다.

---

## 📱 2. 화면 구성 (Screen UI Flow)
* **1. 로그인 화면 (Login):** JWT 기반 사용자 인증
* **2. 상품 목록 화면 (Product List):** 판매 중인 한정판 상품 리스트 조회 (캐싱 적용)
* **3. 상품 상세 화면 (Product Detail):** 상품 정보 및 잔여 재고 확인
* **4. 주문/결제 화면 (Checkout):** 구매하기 버튼 클릭 시 선착순 대기열 및 재고 검증 로직 진입
* **5. 결과 화면 (Order Result):** 주문 성공(영수증) 또는 실패(품절 안내) 출력

---

## ⚙️ 3. API 명세서 (RESTful API)

### [Auth Service]
* `POST /api/v1/auth/login` : 사용자 로그인 및 JWT 발급
* `POST /api/v1/auth/verify` : 토큰 유효성 검증

### [Product Service]
* `GET /api/v1/products` : 상품 목록 조회
* `GET /api/v1/products/{id}` : 상품 상세 및 현재 재고 조회

### [Order Service] (핵심 타겟)
* `POST /api/v1/orders` : 주문 생성 (내부적으로 Redis 재고 차감 후 DB Insert)
* `GET /api/v1/orders/{userId}` : 사용자별 주문 내역 조회

---

## 🗄️ 4. ERD (데이터베이스 모델링)

```mermaid
erDiagram
    USERS {
        bigint id PK
        varchar email
        varchar password
        varchar name
        datetime created_at
    }
    PRODUCTS {
        bigint id PK
        varchar name
        int price
        int total_stock "총 재고"
        datetime created_at
    }
    ORDERS {
        bigint id PK
        bigint user_id FK
        bigint product_id FK
        int quantity
        varchar status "SUCCESS, FAILED"
        datetime created_at
    }
    
    USERS ||--o{ ORDERS : "places"
    PRODUCTS ||--o{ ORDERS : "contains"

---

#### 5. Application Architecture (App 아키텍처)
```markdown
## 🏗️ Application Architecture
MSA(Microservices Architecture) 기반으로 도메인을 분리하여 결합도를 낮추고 확장성을 높였습니다.

```mermaid
graph TD
    Client[Client / Browser] --> API_GW[API Gateway]
    API_GW --> Auth[Auth Service]
    API_GW --> Product[Product Service]
    API_GW --> Order[Order Service]
    
    Auth -.->|Token| API_GW
    Product --> Cache[(Redis Cache)]
    Order --> Redis_Stock[(Redis: DECR 재고차감)]
    Order --> MySQL[(MySQL RDB: Insert)]

---

#### 5. Infra Architecture (인프라 아키텍처)
**(<img width="2112" height="1578" alt="최종 아키텍처 이미지 drawio" src="https://github.com/user-attachments/assets/dffa9eb2-4a22-4fde-93d5-2c2dbc91261f" />
 `![인프라구조도](./infra.png)` )**

```markdown
## 🌐 Infra Architecture 상세 설명
본 프로젝트는 트래픽 유입부터 배포, 모니터링까지 전체 사이클을 고려하여 설계되었습니다.

1. **Traffic Entry:** `k6`를 통한 5,000 VU 부하 테스트 진행. 트래픽은 `MetalLB`를 거쳐 `Nginx Ingress Controller`와 `API Gateway`로 라우팅됩니다.
2. **Auto Scaling (HPA):** Auth, Product, Order 모든 서비스 파드에 HPA(Horizontal Pod Autoscaler)를 적용하여 CPU/Memory 부하 시 자동으로 스케일 아웃됩니다.
3. **Data Integrity (동시성 제어):** 가장 부하가 심한 `Order Service`는 DB로 직행하지 않고, `Redis`의 원자적 연산(`DECR`)을 통해 선착순 100명의 재고를 1차로 검증합니다. 성공한 요청만 `MySQL`에 `INSERT` 되어 병목을 방지합니다.
4. **GitOps CD:** `GitLab CI`에서 빌드된 이미지는 `Container Registry`에 저장되며, `ArgoCD`가 이를 감지하여 K8s 클러스터에 선언적으로 배포(Sync)합니다.
5. **Observability:** `Prometheus`가 각 서비스의 메트릭을 양방향(Pull)으로 수집하며, `Grafana`로 시각화합니다. 임계치 초과 시 `Alertmanager`를 통해 `Slack`으로 실시간 알림을 전송하여 즉각적인 장애 대응이 가능합니다.


---
