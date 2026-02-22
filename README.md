# 🚀 DropX — 트래픽 폭증 대응 인프라 설계 프로젝트

> 한정판 드롭 상황에서 발생하는 **순간 트래픽 폭증(100x)** 을 안정적으로 처리하기 위한  
> **Kubernetes 기반 GitOps 인프라 설계 및 구축 프로젝트**

---

# 📌 1. 프로젝트 개요 (Overview)

DropX는 특정 시간에 사용자 요청이 폭증하는 환경을 가정하여,

- 자동 확장 (Auto Scaling)
- 트래픽 분산 (Load Balancing)
- 선언형 배포 (GitOps)
- 인프라 복원력 (Resilience)

을 중심으로 **클라우드 네이티브 인프라 설계 역량**을 검증하기 위한 프로젝트입니다.

> ❗ 본 프로젝트는 애플리케이션 기능보다  
> 👉 **인프라 아키텍처 설계 및 구축 능력 검증**에 초점을 둡니다.

---

# 🎯 2. 프로젝트 목표 (Goals)

- Kubernetes 기반 MSA 인프라 설계
- GitOps 기반 선언형 배포 파이프라인 구축
- 트래픽 폭증 상황 대응 아키텍처 구현
- 무중단 확장 구조 검증
- 영속 스토리지(NFS + PVC) 구성

---

# 🧱 3. Infra Architecture

## 📊 전체 아키텍처

![infra-architecture](./docs/images/architecture.png)

---

## 🔄 요청 흐름 (Traffic Flow)


User
→ MetalLB (External IP)
→ Ingress Controller (Nginx)
→ Service (ClusterIP)
→ Application Pod
→ Redis / Database / NFS


---

## 🧩 핵심 구성 요소

### 🖥️ Kubernetes Cluster

- Container Runtime: containerd
- CNI: Calico
- External LoadBalancer: MetalLB
- Ingress: Nginx Ingress Controller

---

### 🚀 CI/CD & GitOps

- GitLab: Source / Registry
- GitLab Runner: CI Pipeline
- ArgoCD: CD (GitOps)

**배포 흐름**


Developer → GitLab push
→ GitLab CI build & push
→ GitOps Repo tag update
→ ArgoCD sync
→ Kubernetes deploy


---

### 📦 Storage Architecture

| 구성 | 역할 |
|------|------|
| NFS Server | 영속 스토리지 제공 |
| StorageClass | 동적 프로비저닝 |
| PVC | Pod 스토리지 요청 |
| PV | 실제 볼륨 |

**설계 의도**

- Pod 재생성 시 데이터 보존
- Stateful 워크로드 대응
- 로그/업로드 파일 영속화

---

### ⚡ Auto Scaling

- HPA 기반 Pod 자동 확장
- 트래픽 증가 대응
- 리소스 효율화

---

# 🏗 4. Application Architecture

> 애플리케이션은 인프라 검증을 위한 **경량 MSA 구조**로 구성

## 서비스 구성

- frontend
- api
- worker (optional)
- redis

---

## 서비스 호출 흐름


Frontend → API → Redis/DB


---

# 📂 5. Repository Structure


dropx/
├─ app-repo/
├─ gitops-repo/
├─ helm-charts/
├─ manifests/
├─ docs/
│ └─ images/
└─ README.md


---

# 🧪 6. 검증 시나리오 (Test Scenarios)

- [ ] ArgoCD GitOps 동기화 확인  
- [ ] HPA 자동 확장 테스트  
- [ ] Pod 장애 복구 테스트  
- [ ] NFS PVC 데이터 유지 확인  
- [ ] Rolling Update 무중단 배포 검증  

---

# 📈 7. Observability (Optional but Recommended)

> 현재 단계: 선택 적용

- Prometheus (metrics)
- Grafana (dashboard)
- AlertManager (alert)

---

# 🚧 8. 향후 고도화 계획 (Roadmap)

- [ ] Prometheus + Grafana 정식 도입
- [ ] Redis HA 구성
- [ ] Multi-node control plane
- [ ] ArgoCD HA
- [ ] Blue/Green 또는 Canary 배포
- [ ] Service Mesh (Istio) 검토

---

# 👤 9. Author

**김영찬**

- Kubernetes / GitOps / Infra Engineering
- Vibe-Bridge Project

---

# 📎 10. 참고

본 프로젝트는 실제 운영 환경을 단순화하여  
**인프라 설계 역량 검증**을 목적으로 제작되었습니다.
