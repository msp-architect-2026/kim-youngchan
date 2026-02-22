#  DropX — 대규모 선착순 한정판 주문 시스템 (High-Concurrency Order System)

> **5,000 VU 트래픽 폭증 상황에서도 데이터 정합성을 보장하는 Kubernetes 기반 GitOps 주문 인프라**

---

##  1. 프로젝트 개요 (Overview)

DropX는 한정판 상품 드롭(Drop) 시 발생하는 **Spike Traffic(순간 트래픽 폭증)** 상황을 해결하기 위해 설계되었습니다.  
애플리케이션의 단순 기능을 넘어, **대규모 트래픽을 견디는 인프라 복원력**과 **데이터 정합성 확보**를 목표로 합니다.

- **핵심 목표:** 동시 접속자 5,000명 대응 및 재고 음수 발생 방지  
- **중점 기술:** Kubernetes(HPA), Redis(Atomic Operation), GitOps(ArgoCD), Observability

---
,
##  2. System Architecture

###  2.1 Infra Architecture (인프라 구조도)

![인프라구조도](https://github.com/user-attachments/assets/dffa9eb2-4a22-4fde-93d5-2c2dbc91261f)

#### 핵심 설계 디테일

1. **Traffic Entry**  
   - `k6` 기반 5,000 VU 부하 테스트 수행  
   - `MetalLB` + `Nginx Ingress`로 외부 트래픽 수용  

2. **Auto Scaling**  
   - 모든 마이크로서비스(`Auth`, `Product`, `Order`)에 **HPA 적용**  
   - 부하 증가 시 파드 자동 확장  

3. **Data Integrity**  
   - 고부하 `Order Service`에 **Redis Atomic 연산(DECR)** 적용  
   - DB 병목 방지 및 재고 정합성 확보  

4. **GitOps CD**  
   - `GitLab CI` → `ArgoCD` 연동  
   - 코드 푸시부터 클러스터 반영까지 자동 Sync  

5. **Observability**  
   - `Prometheus` 메트릭 수집  
   - 장애 발생 시 `Slack` 실시간 알림  

---

###  2.2 Application Architecture (서비스 구조도)

```mermaid
graph TD
    Client[Client / Browser] --> API_GW[API Gateway]
    API_GW --> Auth[Auth Service]
    API_GW --> Product[Product Service]
    API_GW --> Order[Order Service]

    Auth -.->|JWT Token| API_GW
    Product --> Cache[(Redis Cache)]
    Order --> Redis_Stock[(Redis: DECR 재고차감)]
    Order --> MySQL[(MySQL RDB: Insert)]
```

---

##  3. 화면 구성 및 API (Interface)

###  화면 흐름 (UI Flow)
* **로그인:** JWT 기반 사용자 인증 및 보안 세션 유지
* **상품 목록/상세:** Redis 캐싱을 통한 빠른 정보 조회 및 실시간 재고 확인
* **주문/결제:** 구매 클릭 시 Redis 기반 대기열 및 재고 검증 로직 진입

###  주요 API 명세
| 서비스 | 엔드포인트 | 설명 |
| :--- | :--- | :--- |
| **Auth** | `POST /api/v1/auth/login` | 사용자 로그인 및 토큰 발급 |
| **Product** | `GET /api/v1/products/{id}` | 상품 정보 및 현재 재고 조회 |
| **Order** | `POST /api/v1/orders` | **핵심:** Redis 재고 선차감 후 DB 저장 |

---

##  4. 데이터베이스 모델링 (ERD)

```mermaid
erDiagram
    USERS {
        bigint id PK
        varchar email
        varchar password
        varchar name
    }
    PRODUCTS {
        bigint id PK
        varchar name
        int price
        int total_stock "총 재고"
    }
    ORDERS {
        bigint id PK
        bigint user_id FK
        bigint product_id FK
        int quantity
        varchar status "SUCCESS, FAILED"
    }
    
    USERS ||--o{ ORDERS : "places"
    PRODUCTS ||--o{ ORDERS : "contains"
```

---
