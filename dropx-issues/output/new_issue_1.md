# [Infra] k3s HTTP Registry 연동 설정 (registries.yaml + imagePullSecret)

## 설명 및 목표
k3s 클러스터에서 서비스가 사설 GitLab Container Registry 이미지를 가져올 수 있도록 HTTP Registry 연동과 imagePullSecret을 구성합니다.

## 작업 내용
- registries.yaml 작성 (Registry 주소, 인증 방식)
- imagePullSecret 생성
- 클러스터 내 모든 Deployment에서 imagePullSecret 참조

## 완료 기준
- Deployment가 Private Registry 이미지 Pull 가능
- `kubectl get secret`에서 imagePullSecret 확인

## 산출물
- registries.yaml
- imagePullSecret 생성 매니페스트
