# 🛒 DropX (Drop Experience)

> ⚡ 5,000명 동시 접속 상황에서도 재고 정합성을 보장하고 서버 다운 없이 버티는 Kubernetes 기반 MSA 주문 시스템

---

## 🔹 핵심 목표
- TPS 2,000+ / 평균 응답 시간 < 200ms
- 데이터 유실 0건
- 한정판 드롭(Drop) 이벤트 트래픽 극복

---

## 🏗️ 핵심 아키텍처

![DropX Architecture](./assets/dropx-architecture.png)  
*외부 트래픽 → MetalLB → Nginx Ingress → API Gateway → Auth / Product / Order → Redis/MySQL*

- **MSA 구조**: Auth / Product / Order 서비스 격리로 장애 전파 방지  
- **초저지연 재고 관리**: Redis Lua Script + MySQL 최종 저장  
- **자동 확장**: HPA 기반 Order Service 1 → 5 Pod 확장  
- **데이터 영속성**: StatefulSet + PVC  
- **GitOps 배포**: GitLab CI + ArgoCD

---

## ⚡ Quick Start

```bash
# 1. Git Clone
git clone https://github.com/<your-org>/DropX.git
cd DropX

# 2. GitOps 배포
kubectl apply -f k8s/

# 3. Load Testing (k6)
k6 run tests/spike_test.js
```

---

## 📖 상세 기술 문서
Wiki 페이지에서 아키텍처, ERD, API 명세, 부하 테스트, 트러블슈팅 등 상세 내용을 확인하세요:
- 01-Screen-Composition
- 02-API-Specification
- 03-ERD
- 04-Application-Architecture
- 05-Infrastructure-Architecture
- 06-Performance-Test
- 07-Troubleshooting
