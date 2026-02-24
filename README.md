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

![최종 아키텍처 이미지](https://github.com/msp-architect-2026/kim-youngchan/blob/main/docs/images/%EC%B2%B4%EC%A2%85%20%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98%20%EC%9D%B4%EB%AF%B8%EC%A7%80.drawio.png?raw=true)
