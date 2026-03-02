## Issue #79: 기존 등록된 issue 리스트 텍스트로 추출하기

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/79

### 팀

kim-youngchan (김영찬)

### 주차

W01

### 관련 시나리오

[ github 사용 ]

### 증상

기존 등록한 이슈가 수정이 번거롭고 기존 이슈 등록 리스트를 스크랩 하지 못함.

### 원인

이슈를 등록하면 github UI 상으로는 이슈 리스트들의 전체 텍스트를 한번에 스크랩 하지 못한다.

### 해결 방법

GitHub CLI 설치 -> 전체 이슈 텍스트로 한번에 추출 
```bash
sudo apt install gh
gh auth login
gh issue list --limit 100 --json number,title,body > issues.json
```
-> markdown 파일로 정리
```bash
gh issue list --limit 100 --json number,title,body \
  | jq -r '.[] | "## Issue #\(.number)\n### \(.title)\n\(.body)\n\n"' \
  > issues_dump.md
```

### 교훈

Github CLI도 적극 활용하면 업무 활용성이 극대화 될 것 같다.

---

## Issue #78: [CI/CD] Helm 패키지 매니저 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/78

작업 내용 (Task List)
- [x] **Helm v3 설치**: PC 1(Master)에 최신 안정 버전의 Helm 바이너리 설치 및 환경 변수 확인
- [x] **Helm Repo 등록**: `ingress-nginx` 공식 차트 저장소 추가 및 로컬 캐시 업데이트

완료 기준 (DoD)
- [x] **helm version**: 명령 시 클라이언트 버전 정보가 정상적으로 출력됨

---

## Issue #77: [ Final ] 전체 시스템 통합 테스트 및 최종 보고서 작성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/77

- **설명**: 지금까지 구축한 인프라와 기능, 전체 흐름이 완벽한지 최종 점검 후 문서화 및 포트폴리오 작성을 진행합니다.
- **작업 내용**:
    - [ ] 전체 파이프라인(Git 커밋 -> 빌드 -> 배포 -> 모니터링) 작동 확인
    - [ ] 시스템 아키텍처 다이어그램 및 기술 스택 문서화
- **완료 기준 (DoD)**:
    - [ ] 최종 결과 보고서 완료 및 프로젝트 README 최신화
    - [ ] 기준에 맞춘 포트폴리오 작성을 완료합니다

---

## Issue #76: [ UI ] 최종 데모 리허설

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/76

- **설명**: 프런트엔드부터 인프라까지 모든 레이어의 연동 상태를 최종 점검하고 실전 데모를 준비합니다.
- **작업 내용**:
    - [ ] 전체 환경(Full-stack + Infra) 통합 테스트 수행
    - [ ] 부하 상황 중 장애 주입 및 자동 복구 시나리오 실제 구동
- **완료 기준 (DoD)**:
    - [ ] 리허설 도중 치명적인 버그 없이 시나리오 완주 성공

---

## Issue #75: [ UI ] Admin Dashboard 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/75

- **설명**: 시스템 관리자가 현재 서비스 상태를 모니터링하고, 필요 시 즉시 장애 주입을 제어할 수 있는 관리자 화면을 개발합니다.
- **작업 내용**:
    - [ ] Prometheus/Grafana 지표 연동(차트 라이브러리 활용)
    - [ ] Admin API 기반의 'Kill-Pod' 제어 버튼 배치
- **완료 기준 (DoD)**:
    - [ ] 실시간 트래픽/에러율 지표 시각화 성공
    - [ ] 관리자 페이지에서 버튼 클릭 시 실제 Pod 삭제 명령 전달 확인

---

## Issue #74: [ UI ] Drop Detail Page 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/74

- **설명**: 특정 상품의 상세 정보와 사이즈별 실시간 재고 상태를 보여주는 페이지를 구현합니다.
- **작업 내용**:
    - [ ] 상품 상세 정보 API 연동
    - [ ] 재고 조회 API를 통한 사이즈별 잔여 수량 실시간 렌더링
- **완료 기준 (DoD)**:
    - [ ] 사이즈 선택 시 해당 사이즈의 재고 존재 여부가 정확히 반영됨
    - [ ] 품절(Sold Out) 상태 시 구매 버튼 비활성화 확인

---

## Issue #73: [ UI ] Drop Landing Page 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/73

- **설명**: 사용자가 처음 접속했을 때 상품 리스트와 드롭 시작 시간을 직관적으로 확인할 수 있는 메인 페이지를 개발합니다.
- **작업 내용**:
    - [ ] 상품 목록 API 연동 및 카드 UI 컴포넌트 개발
    - [ ] 드롭 카운트다운(Countdown) 타이머 구현
- **완료 기준 (DoD)**:
    - [ ] 페이지 접속 시 백엔드로부터 상품 데이터를 정상적으로 불러옴
    - [ ] 드롭 시작 전/후의 UI 상태 변경 확인

---

## Issue #72: [ CronJob ] K3s CronJob 배포 및 로그 기록

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/72

- **설명**: 정합성 체크 스크립트를 쿠버네티스 CronJob 리소스로 등록하여 주기적으로 자동 실행하고, 그 결과를 별도의 로그 테이블이나 파일로 기록합니다.
- **작업 내용**:
    - [ ] 정합성 체크 앱 도커 이미지 빌드 및 Manifest(CronJob) 작성
    - [ ] `ConsistencyLogs` 테이블 생성 및 체크 결과 INSERT 로직 연결
- **완료 기준 (DoD)**:
    - [ ] `kubectl get cronjob` 상태 확인 및 스케줄에 따른 자동 실행 확인
    - [ ] 실행 후 DB 또는 로그 시스템에 검증 결과 레코드가 정상적으로 적재됨

---

## Issue #71: [ CronJob ] Redis ↔ MySQL 정합성 체크 로직 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/71

- **설명**: 한정판 드롭 이벤트 종료 후, Redis의 잔여 재고 수치와 MySQL에 기록된 실제 주문 건수의 합계가 일치하는지 비교하는 검증 로직을 구현합니다.
- **작업 내용**:
    - [ ] Redis `stock:{id}` 값과 MySQL `Orders` 테이블의 성공 건수 합산 비교 스크립트 작성
    - [ ] 수치 불일치(Inconsistency) 발생 시 상세 내역을 추출하는 예외 로직 작성
- **완료 기준 (DoD)**:
    - [ ] 검증 스크립트 실행 시 정합성 결과(일치/불일치)가 콘솔 또는 로그에 명확히 출력됨

---

## Issue #70: [ LoadTest ] Kill-Pod 장애 주입 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/70

- **설명**: 고부하 상황에서 특정 Pod이 강제 종료되었을 때, 전체 주문 성공률에 미치는 영향과 시스템의 복구 능력을 검증합니다.
- **작업 내용**:
    - [ ] 5,000 VU 부하가 진행 중인 상태에서 `Admin API Kill-Pod` 호출
    - [ ] Pod 재생성 시간 동안의 에러율 및 주문 성공률 데이터 수집
- **완료 기준 (DoD)**:
    - [ ] 장애 인입 시에도 서비스가 가용성을 유지하는지 확인
    - [ ] 부하 종료 후 주문 성공/실패율 및 복구 시간 리포트 작성

---

## Issue #69: [ LoadTest ] 5,000 VU 스파이크 테스트 수행

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/69

- **설명**: 한정판 드롭 오픈 직후의 폭발적인 트래픽을 가정하여 시스템의 처리량(Throughput)과 지연 시간(Latency)을 측정합니다.
- **작업 내용**:
    - [ ] k6 스파이크 테스트(Spike Test) 실행 (순간 부하 인입)
    - [ ] 시스템 메트릭(CPU, Memory, Redis Connection) 모니터링
- **완료 기준 (DoD)**:
    - [ ] p95 지연 시간(Latency) 200ms 이하 유지
    - [ ] 5,000 VU 환경에서 시스템 다운 없이 안정적 처리 확인

---

## Issue #68: [ LoadTest ] k6 테스트 시나리오 작성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/68

- **설명**: 실제 사용자의 이용 패턴(로그인 → 상품 조회 → 재고 선점 → 주문 확정)을 모사한 k6용 JavaScript 테스트 시나리오를 작성합니다.
- **작업 내용**:
    - [ ] 시나리오별 API 엔드포인트 및 Payload 정의
    - [ ] 5,000 VU(Virtual Users) 할당을 위한 리소스 계획 수립
- **완료 기준 (DoD)**:
    - [ ] 소량의 VU로 실행 시 전체 시퀀스 에러 없이 통과
    - [ ] `k6 run` 시나리오 파일 문법 오류 없음 확인

---

## Issue #67: [ Auto ] Admin API 'Kill-Pod' 기능 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/67

- **설명**: 고의적인 장애 상황 테스트 또는 긴급 조치를 위해 특정 Pod을 강제로 종료하는 관리자 전용 API를 구현합니다.
- **작업 내용**:
    - [ ] `order-admin` ServiceAccount에 Pod 삭제(Delete) 권한 부여 (RBAC 설정)
    - [ ] 해당 권한을 사용하는 API 엔드포인트 개발
- **완료 기준 (DoD)**:
    - [ ] API 호출 시 대상 Pod이 삭제되고, ReplicaSet/HPA에 의해 즉시 새로운 Pod이 재생성되는지 확인

---

## Issue #66: [ Auto ] PDB(Pod Disruption Budget) 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/66

- **설명**: 자발적인 중단(Rolling Update, Node 유지보수 등) 상황에서도 서비스 가용성을 보장하기 위해 최소한으로 유지되어야 하는 Pod 수를 정의합니다.
- **작업 내용**:
    - [ ] `minAvailable: 1` 설정을 포함한 PDB 리소스 배포
- **완료 기준 (DoD)**:
    - [ ] `kubectl get pdb` 결과 확인
    - [ ] 노드 드레인(Drain)이나 업데이트 시에도 서비스가 중단되지 않고 최소 1개 이상의 Pod이 유지됨을 검증

---

## Issue #65: [ Auto ] HPA(Horizontal Pod Autoscaler) 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/65

- **설명**: 트래픽 증가 시 시스템 부하를 분산하기 위해 CPU 사용량에 따라 Pod의 개수를 자동으로 확장/축소하도록 설정합니다.
- **작업 내용**:
    - [ ] Metrics Server 설치 여부 확인
    - [ ] CPU 사용률 60% 기준, 최소 1개에서 최대 5개까지 스케일링 정책 적용
- **완료 기준 (DoD)**:
    - [ ] `kubectl get hpa` 명령 시 설정한 Target과 Min/Max 수치가 정상 표시됨
    - [ ] 부하 테스트(Stress) 시 Pod 수가 자동으로 증가하는지 확인

---

## Issue #64: [ Monitoring ] Alertmanager 설치 + Slack 연동

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/64

- **설명**: 장애 상황(Pod 다운, 응답 지연 등) 발생 시 담당자에게 즉시 알림이 가도록 설정합니다.
- **작업 내용**:
    - [ ] Alertmanager 설치 및 Slack Webhook 연동 설정
    - [ ] 임계값 기반 알람 규칙(Alerting Rule) 정의
- **완료 기준 (DoD)**:
    - [ ] 테스트 알람 발생 시 Slack 채널로 알림 메시지가 정상 수신됨 확인

---

## Issue #63: [ Monitoring ] Grafana 대시보드 구성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/63

- **설명**: 서비스 운영 상태를 한눈에 파악할 수 있도록 핵심 지표(RPS, Error Rate, Latency 등) 대시보드를 구축합니다.
- **작업 내용**:
    - [ ] Kubernetes 클러스터 모니터링 및 개별 서비스 메트릭 시각화
    - [ ] 주요 4대 황금 지표(Latent, Traffic, Errors, Saturation) 패널 구성
- **완료 기준 (DoD)**:
    - [ ] Grafana 대시보드에서 실시간 데이터가 차트로 정상 렌더링됨 확인

---

## Issue #62: [ Monitoring ] Grafana 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/62

- **설명**: Prometheus에서 수집한 데이터를 시각화하여 대시보드로 보여줄 Grafana를 설치합니다.
- **작업 내용**:
    - [ ] Helm을 사용하여 Grafana 설치 및 서비스 노출
    - [ ] Prometheus를 데이터 소스(Data Source)로 등록
- **완료 기준 (DoD)**:
    - [ ] Grafana 로그인 페이지 접속 확인 및 데이터 소스 연결 테스트 성공

---

## Issue #61: [ Monitoring ] Prometheus 스크랩 타겟 확인

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/61

- **설명**: 수집 대상(Node Exporter, Kube-State-Metrics 등)으로부터 메트릭이 정상적으로 들어오는지 확인합니다.
- **작업 내용**:
    - [ ] `targets` 페이지에서 각 엔드포인트의 상태(`UP`) 확인
    - [ ] 기본 메트릭(CPU, Memory 사용량 등) 쿼리 테스트
- **완료 기준 (DoD)**:
    - [ ] Prometheus UI 내 Status -> Targets에서 모든 타겟이 `UP` 상태임을 확인

---

## Issue #60: [ Monitoring ] Prometheus 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/60

- **설명**: 클러스터 내 각종 메트릭 데이터를 수집하고 저장하기 위한 시계열 데이터베이스인 Prometheus를 설치합니다.
- **작업 내용**:
    - [ ] Helm Chart(kube-prometheus-stack 등) 또는 Manifest를 이용한 설치
    - [ ] 데이터 보존 기간(Retention) 및 스토리지(PVC) 설정
    - [ ] Node Exporter 배포 (DaemonSet): 각 노드의 하드웨어(CPU, RAM, Disk) 메트릭 수집
- **완료 기준 (DoD)**:
    - [ ] Prometheus 관련 Pod들이 모두 `Running` 상태임
    - [ ] Prometheus 웹 UI에 정상적으로 접속 가능 확인

---

## Issue #59: [ CI/CD ] Auto-Sync 설정 및 배포 자동화 검증

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/59

- **설명**: Git 저장소의 변경사항을 ArgoCD가 감지하여 자동으로 클러스터에 반영하도록 설정합니다.
- **작업 내용**:
    - [ ] ArgoCD Application 생성 및 자동 동기화(Automatic Sync) 옵션 활성화
    - [ ] Git 커밋 후 클러스터의 리소스가 자동으로 업데이트되는지 테스트
- **완료 기준 (DoD)**:
    - [ ] Git 저장소 수정 후 별도 조작 없이 1~3분 내에 Pod 업데이트 확인

---

## Issue #58: [ CI/CD ] Manifest Repository 연동

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/58

- **설명**: 쿠버네티스 설정 파일(YAML)이 관리되는 Git 저장소를 ArgoCD에 연결합니다.
- **작업 내용**:
    - [ ] ArgoCD 'Repositories' 설정에서 GitLab 프로젝트 URL 및 인증 정보 등록
- **완료 기준 (DoD)**:
    - [ ] ArgoCD UI에서 저장소 연결 상태가 'Successful'로 표시됨

---

## Issue #57: [ CI/CD ] ArgoCD 설치 (PC #1)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/57

- **설명**: 선언적인 GitOps 배포를 위해 Kubernetes 클러스터(PC #1) 내에 ArgoCD를 설치합니다.
- **작업 내용**:
    - [ ] ArgoCD 네임스페이스 생성 및 매니페스트 배포
    - [ ] ArgoCD Server UI 접속을 위한 서비스 노출 (LoadBalancer 또는 Port-forward)
- **완료 기준 (DoD)**:
    - [ ] ArgoCD 관리 화면 로그인 성공 및 모든 시스템 Pod 정상 기동 확인

---

## Issue #56: [ CI/CD ] Helm Chart 구조 검증 및 배포 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/56

- **설명**: 작성된 템플릿에 문법 오류가 없는지 검사하고 실제 쿠버네티스에 배포해 봅니다.
- **작업 내용**:
    - [ ] `helm lint` 명령어를 통한 템플릿 유효성 검사
    - [ ] `helm install`로 실제 애플리케이션 Pod 배포 및 기동 확인
- **완료 기준 (DoD)**:
    - [ ] 배포된 Pod이 `Running` 상태가 되며, 서비스 접근이 정상적으로 이루어짐

---

## Issue #55: [ CI/CD ] Helm Chart values.yaml 환경별 분리

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/55

- **설명**: 개발(Dev)과 운영(Prod) 환경에 따라 설정값(이미지 태그, 복제본 수 등)을 유연하게 적용할 수 있도록 Helm 구조를 설계합니다.
- **작업 내용**:
    - [ ] `values-dev.yaml`, `values-prod.yaml` 파일 생성 및 변수화
    - [ ] 환경별 리소스 할당량(CPU/Mem) 및 Ingress 호스트네임 분리
- **완료 기준 (DoD)**:
    - [ ] `helm install --values` 옵션을 통해 각기 다른 환경 설정 배포 가능

---

## Issue #54: [ CI/CD ] SSH Key 등록 및 파이프라인 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/54

- **설명**: GitLab과 서버 간의 보안 연결을 설정하고 기본적인 CI 워크플로우를 검증합니다.
- **작업 내용**:
    - [ ] Runner 세션 내 SSH Key 생성 및 GitLab에 Deploy Key 등록
    - [ ] `.gitlab-ci.yml` 작성을 통한 간단한 `echo` 빌드 테스트
- **완료 기준 (DoD)**:
    - [ ] GitLab 프로젝트의 CI/CD 파이프라인이 'Passed' 상태로 완료됨

---

## Issue #53: [ CI/CD ] GitLab Runner 설치 및 태그 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/53

- **설명**: 실제 CI 빌드 및 테스트 스크립트를 실행할 전용 에이전트(Runner)를 구성합니다.
- **작업 내용**:
    - [ ] GitLab Runner 설치 및 서버 등록(Registration)
    - [ ] 특정 Job만 수행하도록 태그(예: `shell`, `k8s`) 설정
- **완료 기준 (DoD)**:
    - [ ] GitLab 관리자 메뉴에서 Runner 상태가 'Online'으로 표시됨

---

## Issue #52: [ CI/CD ] GitLab 서버 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/52

- **설명**: 소스 코드 관리 및 CI 파이프라인의 중심이 될 GitLab 인스턴스를 PC #2에 설치합니다.
- **작업 내용**:
    - [ ] Docker 또는 Linux 패키지를 이용한 GitLab 서버 설치
    - [ ] 초기 루트 비밀번호 설정 및 도메인/IP 접속 환경 구성
- **완료 기준 (DoD)**:
    - [ ] 웹 브라우저에서 GitLab 대시보드 접속 가능 확인
    - [ ] 테스트 계정 생성 및 프로젝트(Repo) 생성 성공

---

## Issue #51: [ Redis ] 실패/타임아웃 시 rollback 처리

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/51

- **설명**: 사용자가 결제를 취소하거나 토큰이 만료(타임아웃)된 경우, 선점했던 재고를 다시 원복시키는 로직을 구현합니다.
- **작업 내용**:
    - [ ] 토큰 만료 이벤트 감지 또는 명시적 취소 시 `INCR` 명령을 통한 재고 복구
    - [ ] MySQL 주문 실패 처리와 Redis 재고 복구의 일관성 보장
- **완료 기준 (DoD)**:
    - [ ] 결제 실패 상황 재연 시, Redis의 `stock` 수치가 초기값으로 정확히 복구됨 확인

---

## Issue #50: [ Redis ] confirm 단계에서 토큰 검증 + MySQL 처리

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/50

- **설명**: 사용자가 결제를 완료했을 때, 선점한 토큰의 유효성을 검증하고 최종적으로 MySQL에 주문 데이터를 확정합니다.
- **작업 내용**:
    - [ ] Redis에서 토큰 존재 여부 및 소유권 검증 로직 구현
    - [ ] 검증 성공 시 MySQL 트랜잭션과 연동하여 최종 주문 상태 업데이트
- **완료 기준 (DoD)**:
    - [ ] 유효한 토큰일 때만 MySQL 레코드가 생성/업데이트됨 확인

---

## Issue #49: [ Redis ] reserve_token 생성 + TTL 적용

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/49

- **설명**: 2단계 확정(2-Phase Confirm) 로직을 위해, 재고 선점 시 임시 토큰을 발행하고 자동 만료 시간을 설정합니다.
- **작업 내용**:
    - [ ] 재고 차감 성공 시 UUID 기반 `reserve_token` 생성 로직 구현
    - [ ] 결제 대기 시간(예: 5분)을 고려한 Redis TTL(Time-To-Live) 적용
- **완료 기준 (DoD)**:
    - [ ] Redis 내에 토큰이 생성되고, 지정된 시간(`EXPIRE`) 후 자동 삭제되는지 확인

---

## Issue #48: [ Redis ] Lua Script 단위 테스트 작성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/48

- **설명**: 작성된 Lua Script가 다양한 상황(재고 부족, 키 미존재 등)에서 의도대로 동작하는지 검증합니다.
- **작업 내용**:
    - [ ] 정상 재고 차감 시나리오 테스트
    - [ ] Edge Case(재고가 딱 0일 때, 요청 수량이 남은 재고보다 많을 때) 테스트
- **완료 기준 (DoD)**:
    - [ ] 모든 테스트 케이스 통과
    - [ ] 예상치 못한 입력에 대해 스크립트가 런타임 에러 없이 설계된 에러 코드 반환

---

## Issue #47: [ Redis ] stock:{s_id}:{size} 조회 및 DECR 원자적 스크립트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/47

[ Redis ] stock:{s_id}:{size} 조회 및 DECR 원자적 스크립트
- **설명**: 여러 요청이 동시에 들어와도 재고가 정확히 감소하도록 Redis 내부에서 원자적으로 실행되는 Lua Script를 작성합니다.
- **작업 내용**:
    - [ ] 재고 확인(GET) 및 차감(DECR) 로직을 포함한 `.lua` 파일 작성
    - [ ] 재고가 0 미만이 될 경우 차감을 거부하고 에러 코드를 반환하는 예외 처리
- **완료 기준 (DoD)**:
    - [ ] `EVAL` 명령어를 통한 스크립트 실행 시 원자적 재고 감소 확인
    - [ ] 동시 다발적 요청 상황에서도 Race Condition 발생 없이 정확한 수치 유지

---

## Issue #46: [ Backend ] 트랜잭션 처리 + 동시성 검증

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/46

- **설명**: 주문 확정 시 재고 차감과 주문 상태 변경을 하나의 트랜잭션으로 처리하여 데이터 무결성을 보장합니다.
- **작업 내용**:
    - [ ] DB Transaction (Begin/Commit/Rollback) 적용
    - [ ] 동시성 테스트 도구(JMeter, Locust 등)를 이용한 경쟁 상태(Race Condition) 방어 확인
- **완료 기준 (DoD)**:
    - [ ] 수백 건의 동시 요청에도 재고 숫자가 음수가 되지 않고 정확히 일치함

---

## Issue #45: [ Backend ] 주문 이력 조회 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/45

- **설명**: 로그인한 사용자가 본인의 과거 주문 내역을 확인할 수 있는 기능을 구현합니다.
- **작업 내용**:
    - [ ] JWT에서 추출한 사용자 ID를 기반으로 주문 테이블 조회
- **완료 기준 (DoD)**:
    - [ ] 본인의 주문 내역만 정확히 필터링되어 반환됨 확인

---

## Issue #44: [ Backend ] 주문 생성 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/44

- **설명**: 사용자의 주문 요청을 수신하여 기본 유효성을 검증하고 임시 주문 기록을 생성합니다.
- **작업 내용**:
    - [ ] 주문 정보(사용자 ID, 상품 ID, 사이즈 등) 수신 및 유효성 검사
- **완료 기준 (DoD)**:
    - [ ] 주문 생성 시 MySQL `Orders` 관련 테이블에 신규 레코드 생성 확인

---

## Issue #43: [ Backend ] 드롭 시간 기반 조회 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/43

- **설명**: 한정판 판매 시작 시간(Drop Time)을 기준으로 필터링하여 상품 목록을 제공합니다.
- **작업 내용**:
    - [ ] 현재 시간 또는 특정 시간을 파라미터로 받아 조건부 쿼리 수행
- **완료 기준 (DoD)**:
    - [ ] 드롭 시간이 지나지 않은 상품이 목록에서 제외되거나 별도 표시됨 확인

---

## Issue #42: [ Backend ] 사이즈별 재고 조회 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/42

- **설명**: 특정 상품의 사이즈별 실시간 재고를 확인하기 위해 MySQL 또는 Redis 데이터를 조회합니다.
- **작업 내용**:
    - [ ] 상품 ID 기반 사이즈별 잔여 수량 조회 로직 작성
- **완료 기준 (DoD)**:
    - [ ] 요청한 상품의 사이즈별 재고 숫자가 데이터베이스 값과 일치함

---

## Issue #41: [ Backend ] 상품 조회 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/41

- **설명**: 전체 상품 리스트를 조회하여 사용자에게 반환하는 읽기 전용 API를 구현합니다.
- **작업 내용**:
    - [ ] MySQL `Sneakers` 테이블 연동 및 데이터 매핑
- **완료 기준 (DoD)**:
    - [ ] GET 요청 시 전체 상품 목록이 JSON 형태로 정상 출력됨

---

## Issue #40: [ Backend ] JWT 검증 미들웨어 작성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/40

- **설명**: 보호된 리소스에 접근할 때 요청 헤더의 JWT를 파싱하고 유효성을 검사하는 공통 미들웨어를 작성합니다.
- **작업 내용**:
    - [ ] Token 서명 검증 및 만료 여부 체크 로직 구현
    - [ ] 인증 실패 시 401 Unauthorized 에러 처리
- **완료 기준 (DoD)**:
    - [ ] 유효하지 않은 토큰으로 요청 시 접근 차단 확인
    - [ ] 만료된 토큰에 대해 적절한 에러 메시지 반환 확인

---

## Issue #39: [ Backend ] 로그인 API + JWT 발급 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/39

- **설명**: 사용자 인증을 수행하고, 향후 요청 시 인증 수단으로 사용할 JWT(JSON Web Token)를 발급합니다.
- **작업 내용**:
    - [ ] ID/PW 일치 여부 검증 로직 구현
    - [ ] Access Token(필요 시 Refresh Token 포함) 생성 및 반환
- **완료 기준 (DoD)**:
    - [ ] 로그인 성공 시 유효한 JWT 토큰이 응답 바디 또는 쿠키에 포함됨

---

## Issue #38: [ Backend ] 회원가입 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/38

- **설명**: 신규 사용자 정보를 수신하여 비밀번호 해싱 후 MySQL 데이터베이스에 저장하는 로직을 구현합니다.
- **작업 내용**:
    - [ ] 사용자 엔티티(Entity) 정의 및 DTO 설계
    - [ ] 비밀번호 암호화(BCrypt 등) 적용 및 DB 연동 로직 작성
- **완료 기준 (DoD)**:
    - [ ] POST 요청 시 201 Created 응답 확인
    - [ ] MySQL에서 `SELECT` 쿼리로 저장된 사용자 레코드 확인

---

## Issue #37: [ DB ] Redis 클라이언트 기반 데이터 최종 검증

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/37

- **설명**: 애플리케이션에서 사용할 Redis 라이브러리 또는 클라이언트를 통해 데이터 정밀 검증을 수행합니다.
- **작업 내용**:
    - [ ] 실제 데이터 타입(String, Hash 등)과 값이 설계와 일치하는지 전수 확인
- **완료 기준 (DoD)**:
    - [ ] 모든 초기 재고 데이터의 정합성이 기획서와 일치함

---

## Issue #36: [ DB ] 초기 재고 데이터 수동 로드

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/36

- **설명**: 드롭 이벤트를 위해 Redis에 실시간 재고 관리용 초기 데이터를 입력합니다.
- **작업 내용**:
    - [ ] `stock:{id}:{size}` 형식의 Key-Value 데이터를 Redis에 적재
- **완료 기준 (DoD)**:
    - [ ] `redis-cli`에서 `KEYS stock:*` 검색 시 입력한 데이터가 정상 조회됨

---

## Issue #35: [ DB ] AOF(Append Only File) 활성화 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/35

- **설명**: Redis 서버 장애 발생 시 데이터 유실을 방지하기 위해 모든 쓰기 명령을 기록하는 AOF 기능을 활성화합니다.
- **작업 내용**:
    - [ ] `redis.conf` 또는 ConfigMap을 통해 `appendonly yes` 설정 적용
    - [ ] 설정 적용 후 Redis 재시작
- **완료 기준 (DoD)**:
    - [ ] `redis-cli info persistence` 명령 시 `aof_enabled:1` 확인 및 재시작 후 데이터 유지 검증

---

## Issue #34: [ DB ] Redis StatefulSet 배포 + PVC

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/34

- **설명**: 고성능 캐싱 및 재고 관리를 위한 Redis를 StatefulSet 구조로 배포하고 볼륨을 연결합니다.
- **작업 내용**:
    - [ ] Redis용 PVC 생성 및 StatefulSet 매니페스트 배포
    - [ ] Redis 서비스(Service) 생성을 통한 내부 통신 엔드포인트 확보
- **완료 기준 (DoD)**:
    - [ ] Redis Pod이 `Running` 상태이며 PVC와 정상적으로 바인딩됨

---

## Issue #33: [ DB ] MySQL 접속 및 CRUD 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/33

- **설명**: 배포된 데이터베이스가 정상적으로 데이터를 읽고 쓸 수 있는지 기본 동작을 검증합니다.
- **작업 내용**:
    - [ ] 테스트 데이터 INSERT 수행 및 SELECT 조회 확인
    - [ ] 데이터 UPDATE 및 DELETE를 통한 트랜잭션 정상 동작 확인
- **완료 기준 (DoD)**:
    - [ ] 기본 CRUD 쿼리 수행 시 에러 없이 결과값이 일치함

---

## Issue #32: [ DB ] 초기 DB 스키마 실행

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/32

- **설명**: 애플리케이션 운영에 필요한 기본 테이블 구조(Sneakers, SneakerSizes)를 생성합니다.
- **작업 내용**:
    - [ ] MySQL Pod 내부 접속 또는 외부 클라이언트를 통해 SQL 스크립트 실행
    - [ ] `Sneakers`, `SneakerSizes` 테이블 정의서 적용
- **완료 기준 (DoD)**:
    - [ ] `SHOW TABLES;` 실행 시 생성된 테이블 리스트가 정상 출력됨

---

## Issue #31: [ DB ] MySQL PVC 생성 및 StatefulSet 배포

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/31

- **설명**: 고유한 네트워크 식별자와 영구 저장소가 필요한 MySQL을 위해 StatefulSet과 PVC를 구성합니다.
- **작업 내용**:
    - [ ] MySQL용 PersistentVolumeClaim(PVC) 정의 및 생성
    - [ ] MySQL StatefulSet 매니페스트 작성 및 배포 (Root 패스워드 설정 포함)
- **완료 기준 (DoD)**:
    - [ ] `kubectl get pods`에서 MySQL Pod이 `Running` 상태임
    - [ ] `kubectl get pvc`에서 해당 PVC가 `Bound` 상태임을 확인

---

## Issue #30: [ k3s ] PVC 생성 후 마운트 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/30

- **설명**: 실제 볼륨을 생성하고 Pod에 마운트하여 데이터 읽기/쓰기 및 영속성을 테스트합니다.
- **작업 내용**:
    - [x] 테스트 PVC 생성 및 Pod 연결 후 파일 저장 테스트
- **완료 기준 (DoD)**:
    - [x] Pod 재시작 후에도 PVC 내부 데이터가 유지됨

---

## Issue #29: [ k3s ] local-path StorageClass 확인

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/29

- **설명**: k3s 기본 스토리지 클래스인 `local-path`가 정상 작동하는지 점검합니다.
- **작업 내용**:
    - [x] `kubectl get sc`를 통해 기본 스토리지 클래스 지정 여부 확인
- **완료 기준 (DoD)**:
    - [x] `local-path` 스토리지 클래스가 존재하고 사용 가능한 상태임

---

## Issue #28: [ k3s ] Nginx Ingress Controller 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/28

- **설명**: L7 라우팅 관리를 위해 표준 Nginx Ingress Controller를 설치합니다.
- **작업 내용**:
    - [x] Helm을 이용하여 `ingress-nginx` 설치 및 서비스 상태 확인
- **완료 기준 (DoD)**:
    - [x] Ingress Controller Pod가 정상적으로 `Running` 상태임

---

## Issue #27: [ k3s ] LoadBalancer Service 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/27

- **설명**: 실제 배포된 서비스에 외부 IP가 할당되고 통신이 가능한지 확인합니다.
- **작업 내용**:
    - [x] 테스트용 Nginx 배포 후 `type: LoadBalancer`로 서비스 노출
- **완료 기준 (DoD)**:
    - [x] 할당된 외부 IP로 HTTP 접속 성공

---

## Issue #26: [ k3s ] L2 모드 IP Pool 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/26

- **설명**: MetalLB가 외부 접근용으로 사용할 IP 주소 대역(예: 192.168.10.230-235)을 정의합니다.
- **작업 내용**:
    - [x] `IPAddressPool` 및 `L2Advertisement` 설정 파일 적용
- **완료 기준 (DoD)**:
    - [x] 설정된 IP 대역이 리소스에 정상 등록됨

---

## Issue #25: [ k3s ] MetalLB 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/25

- **설명**: 온프레미스 환경에서 `LoadBalancer` 타입의 서비스에 IP를 할당하기 위해 MetalLB를 설치합니다.
- **작업 내용**:
    - [x] MetalLB 매니페스트 배포 (Controller 및 Speaker 생성)
- **완료 기준 (DoD)**:
    - [x] `metallb-system` 네임스페이스 내 모든 Pod가 `Running` 상태임

---

## Issue #24: [ k3s ] k3s 경량 Kubernetes 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/24

- **설명**: 리소스 효율성을 위해 기본 로드밸런서와 인그레스(ServiceLB, Traefik)를 제외하고 k3s를 설치합니다.
- **작업 내용**:
    - [x] `curl -sfL https://get.k3s.io | sh -s - --disable servicelb --disable traefik` 실행
    - [x] 노드 상태 확인 및 `/etc/rancher/k3s/k3s.yaml` 권한 설정
- **완료 기준 (DoD)**:
    - [x] `kubectl get nodes` 결과 Master Node가 `Ready` 상태임

---

## Issue #23: [ Infra ] 방화벽 정책 활성화 및 최종 검증

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/23

- **설명**: 설정한 보안 규칙을 실시간으로 적용하고 외부 연결을 테스트합니다.
- **작업 내용**:
    - [ ] `sudo ufw enable` 활성화
    - [ ] `sudo ufw status numbered` 확인
- **완료 기준 (DoD)**:
    - [ ] 외부 PC에서 `nc -zv <IP> 22` 등의 명령으로 포트 오픈 확인

---

## Issue #22: [ Infra ] UFW 방화벽 기본 규칙(Ingress) 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/22

- **설명**: 시스템 보호를 위해 필요한 포트만 개방하는 최소 권한 정책을 적용합니다.
- **작업 내용**:
    - [ ] 허용 포트 등록: `22` (SSH), `6443` (K8s API), `80` (HTTP), `443` (HTTPS)
- **완료 기준 (DoD)**:
    - [ ] `sudo ufw show added`로 등록된 규칙 리스트 확인

---

## Issue #21: [ Infra ] Security & Access (보안 및 접근 제어)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/21

- **설명**: 자동화 스크립트 실행 및 노드 관리를 위해 패스워드 없이 SSH 접속이 가능하게 설정합니다.
- **작업 내용**:
    - [x] PC #2에서 `ssh-keygen` (RSA 4096) 생성
    - [x] `ssh-copy-id` 명령으로 PC #1에 공개키 전송
- **완료 기준 (DoD)**:
    - [x] PC #2에서 PC #1로 접속 시 비밀번호 입력 없이 쉘 획득

---

## Issue #20: [ Infra ] /etc/hosts 매핑 및 상호 호스트 통신 검증

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/20

- **설명**: 내부망에서 IP 대신 호스트네임으로 상호 참조가 가능하도록 설정합니다.
- **작업 내용**:
    - [x] PC 1, 2의 `/etc/hosts` 파일에 상호 `IP - Hostname` 페어 추가
- **완료 기준 (DoD)**:
    - [x] PC 1 ↔ PC 2 간 호스트네임 기반 `ping` 통신 성공

---

## Issue #19: [ Infra ] Netplan 설정을 통한 정적 IP(Static IP) 할당

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/19

- **설명**: 노드 간 통신 안정성을 위해 유동 IP가 아닌 고정 IP 환경을 구축합니다.
- **작업 내용**:
    - [x] `/etc/netplan/*.yaml` 수정 (Address, Gateway, DNS 설정)
    - [x] `sudo netplan apply` 적용

- **완료 기준 (DoD)**:
    - [x] `ip addr` 결과에 설정한 Static IP가 표시됨
    - [x] 재부팅 후에도 동일한 IP 유지 확인

---

## Issue #18: [ Infra ] 운영 필수 공통 패키지 설치

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/18

- **설명**: 효율적인 서버 모니터링 및 트러블슈팅을 위한 유틸리티를 구성합니다.
- **작업 내용**:
    - [x] 필수 도구 설치: `vim`, `git`, `curl`, `net-tools`, `htop`, `tree`
- **완료 기준**:
    - [x] `htop` 실행 시 리소스 모니터링 화면 정상 출력 확인

---

## Issue #17: [ Infra ] 시스템 패키지 최신화 (Update & Upgrade)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/17

- **설명**: 설치 직후 시스템 보안 취약점 패치 및 최신 커널 업데이트를 수행합니다.
- **작업 내용**:
    - [x] `sudo apt update && sudo apt full-upgrade -y` 실행
    - [x] 불필요한 패키지 정리 (`sudo apt autoremove`)
- **완료 기준 **:
    - [x] 재부팅(`reboot`) 후 커널 커럽션 없이 정상 기동 확인

---

## Issue #16: [ Infra ] PC #2 OS 설치 (GitLab/Dev 환경)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/16

- **설명**: 개발 도구 및 CI/CD 환경이 구동될 PC #2의 OS 환경을 준비합니다.
- **작업 내용**:
    - [x] Ubuntu Server 22.04 LTS 설치
    - [ ] 호스트네임 설정 (예: `dev-srv` 또는 `gitlab-node`)
- **완료 기준**:
    - [x] 외부망 통신 확인 (`ping 8.8.8.8`)
    - [x] 원격 터미널에서 SSH 접속 성공

---

## Issue #15: [ Infra ] PC #1 OS 설치 (Kubernetes Master Node)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/15

- **설명**: K8s Control Plane 역할을 수행할 물리/가상 머신에 기반 OS를 구축합니다.
- **작업 내용**:
    - [x] Ubuntu Server 22.04 LTS 설치
    - [x] 시스템 타임존 설정 (`Asia/Seoul`)
    - [x] 기본 관리자 계정 생성 및 sudo 권한 확인
- **완료 기준**:
    - [x] 시스템 부팅 및 로컬 로그인 성공
    - [x] `cat /etc/os-release` 실행 시 버전 22.04 확인

---

## Issue #14: [Docs-01] 프로젝트 Wiki 및 기술 설계 문서 최종 업데이트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/14

### 📝 목적
DropX 프로젝트의 전체 설계, 아키텍처, 테스트 결과 및 트러블슈팅 내용을 
GitHub Wiki에 최종 반영하여 기술적 의사결정과 구현 결과를 문서화한다.

단순 구현 프로젝트가 아닌, 설계 기반 프로젝트임을 명확히 보여주기 위함.

---

### ✅ 업데이트 범위

#### 1️⃣ 01-Screen-Composition
- [ ] 주문 흐름 다이어그램 최신화
- [ ] 인증 → 상품 조회 → 주문 프로세스 UI 흐름 정리

#### 2️⃣ 02-API-Specification
- [ ] Auth / Product / Order API 명세 최종 반영
- [ ] 요청/응답 예시(JSON) 추가
- [ ] 에러 코드 정의 정리

#### 3️⃣ 03-ERD
- [ ] USERS / PRODUCTS / ORDERS 테이블 구조 반영
- [ ] 관계(1:N) 명확화
- [ ] 인덱스 전략 명시 (PK/FK)

#### 4️⃣ 04-Application-Architecture
- [ ] Redis Lua Script 동시성 제어 전략 상세 설명
- [ ] Redis → MySQL 데이터 흐름 시퀀스 다이어그램 추가
- [ ] 재고 음수 방지 구조 설명

#### 5️⃣ 05-Infrastructure-Architecture
- [ ] 전체 Infra 아키텍처 다이어그램 최신화
- [ ] MetalLB → Ingress → Gateway → Service 흐름 정리
- [ ] HPA 동작 구조 설명
- [ ] StatefulSet + PVC 영속성 전략 설명
- [ ] GitLab CI → ArgoCD GitOps 흐름 정리

#### 6️⃣ 06-Performance-Test
- [ ] k6 부하 테스트 시나리오 명시
- [ ] 5,000명 동시접속 결과 정리
- [ ] TPS / 평균 응답시간 / CPU 사용률 기록
- [ ] HPA Scale-out 시점 캡처

#### 7️⃣ 07-Troubleshooting
- [ ] Worker Node 강제 종료 테스트 결과
- [ ] 12초 복구 과정 설명
- [ ] 발생했던 에러 및 해결 과정 정리

---

### 🎯 완료 기준
- Wiki 7개 페이지 모두 최신 설계 기준으로 업데이트 완료
- 모든 아키텍처 다이어그램 최신 버전 반영
- 성능 테스트 수치가 명확히 기록됨
- 면접 시 Wiki를 기반으로 설명 가능

---

### 📊 기대 효과
- 기술적 의사결정 근거 명확화
- 프로젝트 완성도 상승
- 면접 시 설계 중심 프로젝트로 어필 가능

---

### 🔗 연관 이슈
- Infra 관련 이슈 전체
- Backend 관련 이슈 전체
- Observability & Test 관련 이슈 전체

---

## Issue #13: [test-02] Worker Node 강제 종료 테스트

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/13

### 📝 목적
Worker Node 장애 발생 시 Kubernetes Self-Healing 능력을 검증하기 위함.

### ✅ 할 일
- [ ] Worker Node 강제 종료
- [ ] Pod 재스케줄링 시간 측정
- [ ] 서비스 정상 응답 여부 확인
- [ ] 데이터 유실 여부 확인

### 🎯 완료 기준
- 12초 내 Pod 복구
- 서비스 중단 없이 응답 유지
- 데이터 유실 0건

### 🔗 연관 문서
- Wiki: 07-Troubleshooting

---

## Issue #12: EPIC 3: Observability & Test [Test-01] k6 부하 테스트 및 임계치 분석

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/12

### 📝 목적
5,000명 동시접속 상황에서 TPS 및 평균 응답시간을 측정하고 HPA 임계치를 검증하기 위함.

### ✅ 할 일
- [ ] 로그인 API 부하 테스트
- [ ] 상품 조회 부하 테스트
- [ ] 주문 API Spike 테스트
- [ ] 0 → 5,000명 Ramp-up 시나리오 작성
- [ ] TPS 기록
- [ ] 평균 응답시간 기록

### 📊 추가 분석
- CPU 사용률에 따른 Pod 증가 시점 기록
- 60% 기준이 최적인지 검증
- TPS 2,000 이상 유지 여부 확인

### 🎯 완료 기준
- TPS 2,000 이상 달성
- 평균 응답시간 200ms 이하
- 데이터 유실 0건

### 🔗 연관 문서
- Wiki: 06-Performance-Test

---

## Issue #11: [Order-04] Redis ↔ MySQL 정합성 처리 전략 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/11

### 📝 목적
Redis 재고 차감 성공 후 DB 저장 실패 시 데이터 불일치를 방지하기 위함.

### ✅ 할 일
- [ ] DB Insert 예외 처리 로직 구현
- [ ] DB 저장 실패 시 Redis 재고 복구 로직 구현
- [ ] 예외 발생 시 로그 기록
- [ ] 재시도 여부 정책 정의

### 🤔 고려 사항
- DB 저장 실패 시 Redis 재고는 즉시 복구할 것인가?
- 재시도 횟수는 몇 회로 제한할 것인가?

### 🎯 완료 기준
- DB 실패 시 재고 불일치 0건
- 로그 기반 추적 가능

### 🔗 연관 문서
- Wiki: 04-Application-Architecture

---

## Issue #10: [Order-03] 주문 생성 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/10

### 📝 목적
Redis 선차감 성공 요청에 대해서만 MySQL에 주문 데이터를 저장하기 위함.

### ✅ 할 일
- [ ] POST /orders 구현
- [ ] Redis 차감 성공 시 DB Insert
- [ ] 실패 시 400 반환
- [ ] 트랜잭션 처리 확인

### 🎯 완료 기준
- Redis 실패 시 DB Insert 발생하지 않음
- 주문 정상 저장 확인

### 🔗 연관 문서
- Wiki: 02-API-Specification

---

## Issue #9: [Order-02] Redis Lua Script 재고 차감 로직 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/9

### 📝 목적
DB Lock 경합 없이 초당 수천 건의 재고 차감을 원자적으로 처리하기 위함.

### ✅ 할 일
- [ ] Redis Lua Script 작성 (`GET` + `DECR` 원자화)
- [ ] 재고 < 0 방지 로직 포함
- [ ] Script SHA 캐싱 적용
- [ ] k6 기반 단일 Pod 1,000 TPS 테스트

### 🎯 완료 기준
- 동시 요청 상황에서도 재고 음수 발생 0건
- 평균 응답 시간 200ms 이하 유지

### 🔗 연관 문서
- Wiki: 04-Application-Architecture

---

## Issue #8: EPIC 2: Backend & Database [Auth-01] JWT 로그인 API 구현

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/8

### 📝 목적
사용자 인증을 JWT 기반으로 통합 관리하여 MSA 환경에서 인증을 일관되게 처리하기 위함.

### ✅ 할 일
- [ ] 로그인 API 구현
- [ ] JWT 발급 로직 구현
- [ ] Gateway JWT 검증 필터 적용
- [ ] 인증 실패 시 401 반환

### 🎯 완료 기준
- 인증 성공 시 JWT 발급
- 인증 실패 시 접근 차단

### 🔗 연관 문서
- Wiki: 02-API-Specification

---

## Issue #7: [CI/CD-06] GitLab CI & ArgoCD GitOps 파이프라인 구축

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/7

### 📝 목적
코드 변경 사항을 자동으로 빌드하고, 선언적(Declarative) 방식으로 Kubernetes 클러스터에 배포하기 위함.
GitOps 기반 운영을 통해 배포 이력 추적 및 롤백 가능 환경을 구축한다.

---

### ✅ 할 일
- [ ] `.gitlab-ci.yml` 작성
  - [ ] Docker 이미지 Build 단계 구성
  - [ ] Docker Registry Push 단계 구성
  - [ ] 브랜치별 동작 전략 정의 (main / develop 등)
- [ ] GitLab Runner 정상 동작 확인
- [ ] ArgoCD 설치 및 초기 설정
- [ ] ArgoCD Application YAML 작성
- [ ] Git Repository와 ArgoCD 연동
- [ ] Auto-Sync 활성화
- [ ] Git Push → 자동 배포 여부 확인
- [ ] 배포 실패 시 ArgoCD 상태 확인 및 원인 분석

---

### 🎯 완료 기준
- Git Push 시 자동으로 Docker 이미지 빌드 및 Registry Push 성공
- ArgoCD가 변경된 Manifest를 감지하고 자동으로 클러스터에 반영
- ArgoCD Dashboard에서 Application 상태가 `Healthy` 및 `Synced` 상태 확인
- 수동 kubectl apply 없이 배포 가능

---

### 🔍 검증 항목
- 잘못된 이미지 태그 Push 시 배포 실패 여부 확인
- 이전 커밋으로 롤백 가능 여부 확인

---

### 🔗 연관 문서
- Wiki: 05-Infrastructure-Architecture
- Wiki: 07-Troubleshooting

---

## Issue #6: [DB-05] MySQL StatefulSet + PVC 구성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/6

### 📝 목적
Pod 재시작 및 Worker Node 장애 발생 시에도 데이터 유실을 방지하기 위함.

### ✅ 할 일
- [ ] StorageClass 정의 (NFS 기반)
- [ ] PVC 생성
- [ ] MySQL StatefulSet 구성
- [ ] Headless Service 구성
- [ ] Pod 재시작 후 데이터 유지 확인

### 🎯 완료 기준
- MySQL Pod 삭제 후 재생성 시 데이터 유지
- Worker Node 장애 시 재스케줄링 성공

### 🔗 연관 문서
- Wiki: 05-Infrastructure-Architecture
- Wiki: 03-ERD

---

## Issue #5: [K8s-04] Order Service HPA 설정 (CPU 60%)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/5

### 📝 목적
Spike Traffic 상황에서 Order Service의 자동 확장을 통해 서버 다운 없이 트래픽을 처리하기 위함.

### ✅ 할 일
- [ ] HPA YAML 작성 (CPU 60%)
- [ ] minReplicas=1, maxReplicas=5 설정
- [ ] 부하 테스트 중 Scale-out 확인
- [ ] Scale-in 정상 동작 확인
- [ ] CPU 임계치 선택 근거 기록

### 📊 추가 기록
- 5,000명 동시접속 시 평균 CPU 사용률 기록
- CPU 50%, 60%, 70% 기준 비교 후 최적 임계치 판단

### 🎯 완료 기준
- 부하 증가 시 자동 Scale-out
- 부하 감소 시 자동 Scale-in

### 🔗 연관 문서
- Wiki: 05-Infrastructure-Architecture
- Wiki: 06-Performance-Test

---

## Issue #4: [Infra-03] Metrics Server 설치 (HPA 선행 작업)

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/4

### 📝 목적
HPA 동작을 위한 CPU/Memory 메트릭 수집 환경 구축.

### ✅ 할 일
- [ ] Metrics Server 배포
- [ ] kubectl top pod 정상 동작 확인
- [ ] Order Pod CPU 사용량 확인

### 🎯 완료 기준
- kubectl top 명령어 정상 출력
- HPA에서 메트릭 인식 가능

### 🔗 연관 문서
- Wiki: 05-Infrastructure-Architecture

---

## Issue #3: [Infra-02] Nginx Ingress Controller 설치 및 라우팅 구성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/3

### 📝 목적
L7 레벨에서 Path 기반 라우팅을 수행하여 MSA 구조의 각 서비스로 트래픽을 분기하기 위함.

### ✅ 할 일
- [ ] Ingress Controller 배포
- [ ] IngressClass 정의
- [ ] /auth, /products, /orders Path 라우팅 설정
- [ ] 외부 접속 테스트

### 🎯 완료 기준
- 각 Path가 정상적으로 해당 서비스로 전달됨
- 404/502 오류 없이 응답 반환

### 🔗 연관 문서
- Wiki: 05-Infrastructure-Architecture

---

## Issue #2: [k3s] MetalLB 설치 및 IP Pool 구성

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/2

# 설명: PC #1에 Ubuntu Server 22.04 LTS 설치  
# 목표/검증: 설치 완료 후 부팅 가능, ssh 접속 가능

---

## Issue #1: [W01] 실무형 마이크로서비스 운영 플랫폼 구축 및 GitOps 환경 설정

URL: https://github.com/msp-architect-2026/kim-youngchan/issues/1

### 팀

kim-youngchan (김영찬)

### 주차

W01

### 일감 내용

## 🎯 이번 주 목표
- [ ] [cite_start]MetalLB + Nginx Ingress 기반 LoadBalancer 환경 구성 [cite: 69]
- [ ] [cite_start]GitLab CI -> Helm Chart -> ArgoCD 자동 배포 파이프라인 연결 [cite: 131]
- [ ] [cite_start]Online Boutique 애플리케이션 배포 및 정상 동작 확인 [cite: 145]

## 📋 작업 상세 내용 (Vibe Coding 계획)
1. [cite_start]**인프라 구성**: VM 3대 클러스터에 MetalLB를 설치하여 외부 IP 할당 환경 구축 [cite: 131, 144]
2. [cite_start]**GitOps 설정**: GitLab Runner와 ArgoCD를 연동하여 소스 변경 시 자동 배포 트리거 설정 [cite: 58]
3. [cite_start]**애플리케이션 배포**: Helm Chart를 이용하여 마이크로서비스(Online Boutique) 배포 [cite: 142]
4. [cite_start]**검증**: Claude AI가 생성한 YAML 파일을 직접 검토하고 클러스터에 적용 후 동작 확인 [cite: 138, 140, 155]

## 🛠 관련 기술 스택
- Kubernetes (1 Master, 2 Workers)
- GitLab CI, Helm, ArgoCD
- MetalLB, Nginx Ingress

### 산출물

## 📅 산출물 및 기록 계획
- [cite_start]**코드**: `src/` 폴더 내 Helm Chart 및 Manifest 업로드 [cite: 27, 58]
- [cite_start]**Wiki**: 설치 과정 중 발생한 트러블슈팅 및 인프라 구성도 기록 [cite: 26, 91]
- [cite_start]**회고**: 금요일 KPT 양식에 맞춘 주차별 회고 작성 [cite: 62, 91]

### 마감일

2026-02-27

---

