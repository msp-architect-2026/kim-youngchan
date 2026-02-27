# [Infra] Namespace 및 공통 리소스 초기 배포 (ConfigMap/Secret/SA)

## 설명 및 목표
DropX 클러스터에서 공통 Namespace, ConfigMap, Secret, ServiceAccount를 초기 설정하여 서비스 배포 전제조건을 마련합니다.

## 작업 내용
- dropx Namespace 생성
- 공통 ConfigMap 및 Secret 생성
- CronJob 및 Deployment에서 사용할 ServiceAccount 생성

## 완료 기준
- `kubectl get ns`에서 dropx Namespace 존재 확인
- 공통 Secret/ConfigMap/SA가 생성되어 참조 가능

## 산출물
- namespace.yaml
- configmap-global.yaml
- secret-global.yaml
- serviceaccount.yaml
