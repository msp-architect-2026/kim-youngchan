# 🚀 DropX

> **"한정판 운동화 드롭 상황에서 동시성 충돌 방지 및 재고의 음수 없이 주문을 처리하도록 설계된 Kubernetes + GitOps 기반 주문 인프라 플랫폼"**

본 시스템은 한정판 운동화 판매 시나리오를 기반으로 **Redis Atomic 연산**을 통해 재고 정합성을 보장하고, **Kubernetes HPA 및 Pod 장애 상황**에서도 서비스 가용성과 성공률을 유지하는 것을 목표로 합니다.

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

## 🏗 아키텍처

>아래는 본 프로젝트의 쿠버네티스 인프라 아키텍처입니다.

<img width="2106" height="1794" alt="쿠버네티스 아키텍처 drawio" src="https://github.com/user-attachments/assets/81cb4c43-d04c-490e-bcb8-84c10f89b236" />
<br>

---

## 🔄 서비스 흐름도
>아래는 본 프로젝트 아키텍처 흐름을 쉽게 파악하기 위한 이미지입니다.

<img width="2112" height="1578" alt="서비스 흐름도 drawio" src="https://github.com/user-attachments/assets/292681bd-a7ec-4ada-a418-57d424a7befc" />

---
<br>

## 📚 문서 안내

### 📖 Wiki 전체 문서
| 분류 | 문서 명칭 | 설명 |
| :--- | :--- | :--- |
| **🏠 Wiki Home** | [Wiki 메인 페이지](링크) | 프로젝트 전체 개요 및 단계별 설계 문서 |

### 🛠 기술 문서
| 문서 명칭 | 설명 |
| :--- | :--- |
| [🔗 API 명세서](링크) | REST API 엔드포인트 (auth, product, order) 및 Request/Response 스펙 |
| [📊 ERD 및 데이터 모델](링크) | MySQL 스키마 설계 (users, products, orders, order_items) |
| [⚙️ 환경 설정 가이드](링크) | k3s 설치, MetalLB 구성, Registry 연동 단계별 가이드 |
| [🔧 트러블슈팅](링크) | 자주 발생하는 이슈 및 해결 방법 (OOMKilled, ImagePullBackOff 등) |

### 📝 회고 및 이력
| 문서 명칭 | 설명 |
| :--- | :--- |
| [🗓 Sprint 회고](링크) | Phase별 진행 상황 및 개선 사항 |
| [📌 릴리즈 노트](링크) | 버전별 변경 사항 및 배포 이력 |
| [🐛 Known Issues](링크) | 현재 알려진 제약 사항 및 향후 개선 계획 |

---

### 🔍 빠른 링크
- 🚀 **시작하기**: [환경 설정 가이드](링크) → [Registry 설정](링크) → [모니터링 설치](링크)
- 🏗 **아키텍처 이해**: [전체 아키텍처](링크) → [서비스 흐름도](링크)
- 📊 **성능 검증**: [k6 부하 테스트](링크) → [Grafana 대시보드](링크)
- 🔧 **문제 해결**: [트러블슈팅](링크) → [Known Issues](링크)
