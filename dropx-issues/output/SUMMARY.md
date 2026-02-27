[SUMMARY.md](https://github.com/user-attachments/files/25598637/SUMMARY.md)
# DropX Issue Reformatter 실행 가이드

## 📋 변경 요약
- **리포맷 대상**: 77개 이슈 (#2 ~ #78)
- **변경 내용**: 통일된 형식(설명/작업내용/완료기준/산출물) 적용
- **신규 제안**: 7개 누락 이슈 추가 제안

## 🗂️ 생성된 파일 구조
```
output/
├── SUMMARY.md              ← 이 파일 (실행 가이드)
├── update_all_issues.sh    ← 기존 이슈 업데이트 스크립트
├── create_new_issues.sh    ← 신규 이슈 생성 스크립트
├── proposed_new_issues.md  ← 신규 이슈 상세 제안서
├── new_issue_1.md ~ 7.md   ← 신규 이슈 본문 파일
issues/
├── 2.md ~ 78.md            ← 기존 이슈 리포맷 본문 파일
```

## 🚀 실행 방법

### Step 1: 파일을 PC #2(또는 gh CLI 설치된 머신)로 복사
```bash
# 예시: scp로 복사
scp -r output/ issues/ user@192.168.10.100:~/dropx-issues/
```

### Step 2: gh CLI 인증
```bash
sudo apt install gh     # 설치 (미설치 시)
gh auth login           # GitHub 로그인
# → GitHub.com 선택 → HTTPS → Login with a web browser
```

### Step 3: 기존 이슈 업데이트
```bash
cd ~/dropx-issues
chmod +x output/update_all_issues.sh
./output/update_all_issues.sh
```

### Step 4: (선택) 신규 이슈 생성
```bash
chmod +x output/create_new_issues.sh
./output/create_new_issues.sh
```

## ⚠️ 주의사항
1. `gh issue edit`는 issue **body 전체를 교체**합니다 (append 아님)
2. 실행 전 반드시 `issues/*.md` 파일 내용을 검토하세요
3. #1, #79 이슈는 메타/유틸리티 이슈로 리포맷에서 제외했습니다
4. 이미 완료된 이슈(체크박스 [x])도 산출물 추가를 위해 업데이트됩니다

## 📊 리포맷 형식
```markdown
## 설명
[기존 설명 유지]

## 작업 내용
- [ ] 작업 1
- [ ] 작업 2

## 완료 기준
- [ ] 기준 1
- [ ] 기준 2

## 산출물
- 산출물 1 (새로 추가됨)
- 산출물 2 (새로 추가됨)
```
