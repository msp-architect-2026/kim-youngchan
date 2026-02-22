# 🛒 DropX — 대규모 선착순 한정판 주문 시스템 (High-Concurrency Order System)

> **5,000 VU 트래픽 폭증 상황에서도 데이터 정합성을 보장하는 Kubernetes 기반 GitOps 주문 인프라**

---

## 📌 1. 프로젝트 개요 (Overview)

DropX는 한정판 상품 드롭(Drop) 시 발생하는 **Spike Traffic(순간 트래픽 폭증)** 상황을 해결하기 위해 설계되었습니다. 애플리케이션의 단순 기능을 넘어, **대규모 트래픽을 견디는 인프라 복원력**과 **데이터 정합성** 확보를 목적으로 합니다.

- **핵심 목표:** 동시 접속자 5,000명 대응 및 재고 음수 발생 방지
- **중점 기술:** Kubernetes(HPA), Redis(Atomic Operation), GitOps(ArgoCD), Observability

---

## 🏗️ 2. System Architecture

### 🌐 2.1 Infra Architecture (인프라 구조도)
![인프라구조도](https://github.com/user-attachments/assets/dffa9eb2-4a22-4fde-93d5-2c2dbc91261f)

#### [핵심 설계 디테일]
1. **Traffic Entry:** `k6` 기반 5,000 VU 부하 테스트를 수행하며, `MetalLB`와 `Nginx Ingress`를 통해 외부 트래픽을 수용합니다.
2. **Auto Scaling:** 모든 마이크로서비스(`Auth`, `Product`, `Order`)에 **HPA**를 적용하여 리소스 부하 시 파드를 자동 확장합니다.
3. **Data Integrity:** 가장 부하가 심한 `Order Service`는 **Redis의 원자적 연산(DECR)**을 사용하여 재고를 1차 검증함으로써 DB 병목을 방지합니다.
4. **GitOps CD:** `GitLab CI`와 `ArgoCD`를 연동하여 코드 푸시부터 클러스터 반영까지 전 과정을 자동화(Sync)합니다.
5. **Observability:** `Prometheus`가 메트릭을 수집하고, 장애 상황 발생 시 `Slack`으로 실시간 알림을 전송합니다.

### 🏗️ 2.2 Application Architecture (서비스 구조도)



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
