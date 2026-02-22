# 🛒 DropX — 대규모 선착순 한정판 주문 시스템

> **5,000 동시 접속 환경에서도 재고 정합성을 보장하는 Kubernetes 기반 MSA 주문 시스템**

---

## 🎯 프로젝트 개요

DropX는 한정판 상품 판매 시 발생하는 **Spike Traffic (동시 접속 폭증)** 상황을 가정하여,

- 재고 음수 방지 (Data Consistency)
- 자동 확장 (Auto Scaling)
- 무중단 배포 (GitOps)
- 실시간 관측 (Observability)

를 목표로 설계된 **클라우드 네이티브 주문 시스템**입니다.

---

## 🚀 핵심 문제 & 해결 전략

| 문제 | 해결 방식 |
|------|-----------|
| 동시 주문 시 재고 음수 발생 | Redis Atomic 연산(DECR) |
| 주문 트래픽 폭증 | HPA 기반 Auto Scaling |
| 배포 신뢰성 | ArgoCD GitOps |
| 병목 구간 모니터링 | Prometheus + Grafana |

---

## 📱 Screen UI Flow

1. **Login** — JWT 기반 인증  
2. **Product List** — 상품 목록 조회 (Cache 적용)  
3. **Product Detail** — 재고 확인  
4. **Checkout** — 선착순 재고 검증 진입  
5. **Order Result** — 성공/실패 반환  

---

## ⚙️ 핵심 API

### Auth Service
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/verify`

### Product Service
- `GET /api/v1/products`
- `GET /api/v1/products/{id}`

### Order Service (핵심)
- `POST /api/v1/orders`
- `GET /api/v1/orders/{userId}`

---

## 🏗️ Application Architecture

```mermaid
graph TD
    Client --> API_GW
    API_GW --> Auth
    API_GW --> Product
    API_GW --> Order
    Order --> Redis
    Order --> MySQL
