# 🚀 DropX

> **"한정판 운동화 드롭 상황에서 동시성 충돌 방지 및 재고의 음수 없이 주문을 처리하도록 설계된 Kubernetes + GitOps 기반 주문 인프라 플랫폼"**

본 시스템은 한정판 운동화 판매 시나리오를 기반으로 **Redis Atomic 연산**을 통해 재고 정합성을 보장하고, **Kubernetes HPA 및 Pod 장애 상황**에서도 서비스 가용성과 성공률을 유지하는 것을 목표로 합니다.

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
<br>


---

 # 🛠 Tech Stack

### Container & Orchestration
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **Orchestration** | ![K3s](https://img.shields.io/badge/K3s-FFC61C?style=for-the-badge&logo=kubernetes&logoColor=black) | 경량 Kubernetes 클러스터 (control + worker) |
| **Runtime** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=Docker&logoColor=white) | 애플리케이션 컨테이너화 |

### 데이터 스토리지
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **RDBMS** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=MySQL&logoColor=white) | 영속성 계층, 주문 데이터 저장, ACID 보장 |
| **In-Memory DB** | ![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=Redis&logoColor=white) | 재고 선점, Race Condition 방지, 실시간 처리 |

### 백엔드
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **Web Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009485?style=for-the-badge&logo=FastAPI&logoColor=white) | Auth, Product, Order 서비스 |
| **API 보안** | ![JWT](https://img.shields.io/badge/JWT-black?style=for-the-badge&logo=JSON%20web%20tokens) | 인증/권한 관리, 최소 payload(sub, role, exp) |

### 프론트엔드 / UI
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **Framework** | ![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=React&logoColor=black) ![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=Next.js&logoColor=white) | 사용자 및 관리자 화면 구현 |
| **Styling** | ![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=Tailwind-CSS&logoColor=white) | UI 컴포넌트 스타일링 |
| **Visualization** | ![Recharts](https://img.shields.io/badge/Recharts-22b5bf?style=for-the-badge) | 실시간 메트릭/그래프 표시 |

### Observability / Monitoring
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **Metrics** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) | Pod / App / Redis / MySQL 모니터링 |
| **Dashboard** | ![Grafana](https://img.shields.io/badge/Grafana-F46800?style=for-the-badge&logo=Grafana&logoColor=white) | 실시간 KPI 시각화 |
| **Alerting** | ![Alertmanager](https://img.shields.io/badge/Alertmanager-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) | 장애 / 이상 징후 알림 |

### 운영 / 배포 관리
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **CI/CD** | ![GitLab](https://img.shields.io/badge/GitLab_CI-FC6D26?style=for-the-badge&logo=GitLab&logoColor=white) | Git 기반 파이프라인, Helm Chart 빌드 |
| **Helm** | ![Helm](https://img.shields.io/badge/Helm-0F1628?style=for-the-badge&logo=Helm&logoColor=white) | 환경별 앱 배포 템플릿 |
| **CD** | ![ArgoCD](https://img.shields.io/badge/Argo_CD-EF7B4D?style=for-the-badge&logo=Argo-CD&logoColor=white) | GitOps 기반 지속적 배포 |

### 테스트 & 부하 시뮬레이션
| 범주 | 기술 / 도구 | 역할 / 설명 |
| :--- | :--- | :--- |
| **Load Testing** | ![k6](https://img.shields.io/badge/k6-7D64FF?style=for-the-badge&logo=k6&logoColor=white) | 외부 PC에서 5,000 VU 시뮬레이션 |
| **Performance** | ![Prometheus](https://img.shields.io/badge/Prometheus-E6522C?style=for-the-badge&logo=Prometheus&logoColor=white) | p95, Pod scaling, CPU/Memory 확인 |

<br>

> 📖 Detailed Documentation
> 프로젝트의 아키텍처, 기술 선정 근거 및 상세 구현 방법은 Wiki에서 확인하실 수 있습니다.
> * [**Architecture & Tech Stack**](Wiki_링크_주소) : 왜 이 기술들을 선택했는가? (선정 근거 및 비교)

---

## 4️⃣ 아키텍처

>아래는 본 프로젝트의 쿠버네티스 인프라 아키텍처입니다.

<img width="2106" height="1794" alt="쿠버네티스 아키텍처 drawio" src="https://github.com/user-attachments/assets/81cb4c43-d04c-490e-bcb8-84c10f89b236" />
<br>

---

## 5️⃣ 서비스 흐름도
>아래는 본 프로젝트 아키텍처 흐름을 쉽게 파악하기 위한 이미지입니다.

<img width="2112" height="1578" alt="서비스 흐름도 drawio" src="https://github.com/user-attachments/assets/292681bd-a7ec-4ada-a418-57d424a7befc" />

---

## 6️⃣ 문서 안내

| 문서 명칭 | 바로가기 |
| :--- | :--- |
| 📖 **Wiki 전체 문서** | [Wiki 바로가기](#) |
| 🔗 **API 명세** | [API 명세 바로가기](#) |
| 📁 **데이터 모델 및 ERD** | [데이터 모델 바로가기](#) |
| 🛠️ **트러블슈팅** | [트러블슈팅 바로가기](#) |
