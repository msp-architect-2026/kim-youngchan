#!/bin/bash
# ============================================================
# DropX Issue Reformatter - gh CLI Update Script
# 실행 전 확인사항:
#   1. gh auth login 완료
#   2. 올바른 repo에 접근 권한 확인
#   3. issues/ 디렉토리에 .md 파일 존재 확인
# ============================================================

REPO="msp-architect-2026/kim-youngchan"
ISSUES_DIR="$(cd "$(dirname "$0")/../issues" && pwd)"

# 색상 정의
GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

echo "================================================"
echo "DropX Issue Reformatter"
echo "Target Repo: $REPO"
echo "Total Issues: 77"
echo "================================================"
echo ""

# 사전 체크
if ! command -v gh &> /dev/null; then
    echo -e "${RED}❌ gh CLI가 설치되어 있지 않습니다.${NC}"
    echo "설치: sudo apt install gh  또는  brew install gh"
    exit 1
fi

if ! gh auth status &> /dev/null 2>&1; then
    echo -e "${RED}❌ gh auth login이 필요합니다.${NC}"
    exit 1
fi

echo "✅ gh CLI 인증 확인 완료"
echo ""

SUCCESS=0
FAIL=0

# --- Issue #2 ---
echo -n "Updating Issue #2... "
if gh issue edit 2 --repo "$REPO" --body-file "$ISSUES_DIR/2.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #3 ---
echo -n "Updating Issue #3... "
if gh issue edit 3 --repo "$REPO" --body-file "$ISSUES_DIR/3.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #4 ---
echo -n "Updating Issue #4... "
if gh issue edit 4 --repo "$REPO" --body-file "$ISSUES_DIR/4.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #5 ---
echo -n "Updating Issue #5... "
if gh issue edit 5 --repo "$REPO" --body-file "$ISSUES_DIR/5.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #6 ---
echo -n "Updating Issue #6... "
if gh issue edit 6 --repo "$REPO" --body-file "$ISSUES_DIR/6.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #7 ---
echo -n "Updating Issue #7... "
if gh issue edit 7 --repo "$REPO" --body-file "$ISSUES_DIR/7.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #8 ---
echo -n "Updating Issue #8... "
if gh issue edit 8 --repo "$REPO" --body-file "$ISSUES_DIR/8.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #9 ---
echo -n "Updating Issue #9... "
if gh issue edit 9 --repo "$REPO" --body-file "$ISSUES_DIR/9.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #10 ---
echo -n "Updating Issue #10... "
if gh issue edit 10 --repo "$REPO" --body-file "$ISSUES_DIR/10.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #11 ---
echo -n "Updating Issue #11... "
if gh issue edit 11 --repo "$REPO" --body-file "$ISSUES_DIR/11.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #12 ---
echo -n "Updating Issue #12... "
if gh issue edit 12 --repo "$REPO" --body-file "$ISSUES_DIR/12.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #13 ---
echo -n "Updating Issue #13... "
if gh issue edit 13 --repo "$REPO" --body-file "$ISSUES_DIR/13.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #14 ---
echo -n "Updating Issue #14... "
if gh issue edit 14 --repo "$REPO" --body-file "$ISSUES_DIR/14.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #15 ---
echo -n "Updating Issue #15... "
if gh issue edit 15 --repo "$REPO" --body-file "$ISSUES_DIR/15.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #16 ---
echo -n "Updating Issue #16... "
if gh issue edit 16 --repo "$REPO" --body-file "$ISSUES_DIR/16.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #17 ---
echo -n "Updating Issue #17... "
if gh issue edit 17 --repo "$REPO" --body-file "$ISSUES_DIR/17.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #18 ---
echo -n "Updating Issue #18... "
if gh issue edit 18 --repo "$REPO" --body-file "$ISSUES_DIR/18.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #19 ---
echo -n "Updating Issue #19... "
if gh issue edit 19 --repo "$REPO" --body-file "$ISSUES_DIR/19.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #20 ---
echo -n "Updating Issue #20... "
if gh issue edit 20 --repo "$REPO" --body-file "$ISSUES_DIR/20.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #21 ---
echo -n "Updating Issue #21... "
if gh issue edit 21 --repo "$REPO" --body-file "$ISSUES_DIR/21.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #22 ---
echo -n "Updating Issue #22... "
if gh issue edit 22 --repo "$REPO" --body-file "$ISSUES_DIR/22.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #23 ---
echo -n "Updating Issue #23... "
if gh issue edit 23 --repo "$REPO" --body-file "$ISSUES_DIR/23.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #24 ---
echo -n "Updating Issue #24... "
if gh issue edit 24 --repo "$REPO" --body-file "$ISSUES_DIR/24.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #25 ---
echo -n "Updating Issue #25... "
if gh issue edit 25 --repo "$REPO" --body-file "$ISSUES_DIR/25.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #26 ---
echo -n "Updating Issue #26... "
if gh issue edit 26 --repo "$REPO" --body-file "$ISSUES_DIR/26.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #27 ---
echo -n "Updating Issue #27... "
if gh issue edit 27 --repo "$REPO" --body-file "$ISSUES_DIR/27.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #28 ---
echo -n "Updating Issue #28... "
if gh issue edit 28 --repo "$REPO" --body-file "$ISSUES_DIR/28.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #29 ---
echo -n "Updating Issue #29... "
if gh issue edit 29 --repo "$REPO" --body-file "$ISSUES_DIR/29.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #30 ---
echo -n "Updating Issue #30... "
if gh issue edit 30 --repo "$REPO" --body-file "$ISSUES_DIR/30.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #31 ---
echo -n "Updating Issue #31... "
if gh issue edit 31 --repo "$REPO" --body-file "$ISSUES_DIR/31.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #32 ---
echo -n "Updating Issue #32... "
if gh issue edit 32 --repo "$REPO" --body-file "$ISSUES_DIR/32.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #33 ---
echo -n "Updating Issue #33... "
if gh issue edit 33 --repo "$REPO" --body-file "$ISSUES_DIR/33.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #34 ---
echo -n "Updating Issue #34... "
if gh issue edit 34 --repo "$REPO" --body-file "$ISSUES_DIR/34.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #35 ---
echo -n "Updating Issue #35... "
if gh issue edit 35 --repo "$REPO" --body-file "$ISSUES_DIR/35.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #36 ---
echo -n "Updating Issue #36... "
if gh issue edit 36 --repo "$REPO" --body-file "$ISSUES_DIR/36.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #37 ---
echo -n "Updating Issue #37... "
if gh issue edit 37 --repo "$REPO" --body-file "$ISSUES_DIR/37.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #38 ---
echo -n "Updating Issue #38... "
if gh issue edit 38 --repo "$REPO" --body-file "$ISSUES_DIR/38.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #39 ---
echo -n "Updating Issue #39... "
if gh issue edit 39 --repo "$REPO" --body-file "$ISSUES_DIR/39.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #40 ---
echo -n "Updating Issue #40... "
if gh issue edit 40 --repo "$REPO" --body-file "$ISSUES_DIR/40.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #41 ---
echo -n "Updating Issue #41... "
if gh issue edit 41 --repo "$REPO" --body-file "$ISSUES_DIR/41.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #42 ---
echo -n "Updating Issue #42... "
if gh issue edit 42 --repo "$REPO" --body-file "$ISSUES_DIR/42.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #43 ---
echo -n "Updating Issue #43... "
if gh issue edit 43 --repo "$REPO" --body-file "$ISSUES_DIR/43.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #44 ---
echo -n "Updating Issue #44... "
if gh issue edit 44 --repo "$REPO" --body-file "$ISSUES_DIR/44.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #45 ---
echo -n "Updating Issue #45... "
if gh issue edit 45 --repo "$REPO" --body-file "$ISSUES_DIR/45.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #46 ---
echo -n "Updating Issue #46... "
if gh issue edit 46 --repo "$REPO" --body-file "$ISSUES_DIR/46.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #47 ---
echo -n "Updating Issue #47... "
if gh issue edit 47 --repo "$REPO" --body-file "$ISSUES_DIR/47.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #48 ---
echo -n "Updating Issue #48... "
if gh issue edit 48 --repo "$REPO" --body-file "$ISSUES_DIR/48.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #49 ---
echo -n "Updating Issue #49... "
if gh issue edit 49 --repo "$REPO" --body-file "$ISSUES_DIR/49.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #50 ---
echo -n "Updating Issue #50... "
if gh issue edit 50 --repo "$REPO" --body-file "$ISSUES_DIR/50.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #51 ---
echo -n "Updating Issue #51... "
if gh issue edit 51 --repo "$REPO" --body-file "$ISSUES_DIR/51.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #52 ---
echo -n "Updating Issue #52... "
if gh issue edit 52 --repo "$REPO" --body-file "$ISSUES_DIR/52.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #53 ---
echo -n "Updating Issue #53... "
if gh issue edit 53 --repo "$REPO" --body-file "$ISSUES_DIR/53.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #54 ---
echo -n "Updating Issue #54... "
if gh issue edit 54 --repo "$REPO" --body-file "$ISSUES_DIR/54.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #55 ---
echo -n "Updating Issue #55... "
if gh issue edit 55 --repo "$REPO" --body-file "$ISSUES_DIR/55.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #56 ---
echo -n "Updating Issue #56... "
if gh issue edit 56 --repo "$REPO" --body-file "$ISSUES_DIR/56.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #57 ---
echo -n "Updating Issue #57... "
if gh issue edit 57 --repo "$REPO" --body-file "$ISSUES_DIR/57.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #58 ---
echo -n "Updating Issue #58... "
if gh issue edit 58 --repo "$REPO" --body-file "$ISSUES_DIR/58.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #59 ---
echo -n "Updating Issue #59... "
if gh issue edit 59 --repo "$REPO" --body-file "$ISSUES_DIR/59.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #60 ---
echo -n "Updating Issue #60... "
if gh issue edit 60 --repo "$REPO" --body-file "$ISSUES_DIR/60.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #61 ---
echo -n "Updating Issue #61... "
if gh issue edit 61 --repo "$REPO" --body-file "$ISSUES_DIR/61.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #62 ---
echo -n "Updating Issue #62... "
if gh issue edit 62 --repo "$REPO" --body-file "$ISSUES_DIR/62.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #63 ---
echo -n "Updating Issue #63... "
if gh issue edit 63 --repo "$REPO" --body-file "$ISSUES_DIR/63.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #64 ---
echo -n "Updating Issue #64... "
if gh issue edit 64 --repo "$REPO" --body-file "$ISSUES_DIR/64.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #65 ---
echo -n "Updating Issue #65... "
if gh issue edit 65 --repo "$REPO" --body-file "$ISSUES_DIR/65.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #66 ---
echo -n "Updating Issue #66... "
if gh issue edit 66 --repo "$REPO" --body-file "$ISSUES_DIR/66.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #67 ---
echo -n "Updating Issue #67... "
if gh issue edit 67 --repo "$REPO" --body-file "$ISSUES_DIR/67.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #68 ---
echo -n "Updating Issue #68... "
if gh issue edit 68 --repo "$REPO" --body-file "$ISSUES_DIR/68.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #69 ---
echo -n "Updating Issue #69... "
if gh issue edit 69 --repo "$REPO" --body-file "$ISSUES_DIR/69.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #70 ---
echo -n "Updating Issue #70... "
if gh issue edit 70 --repo "$REPO" --body-file "$ISSUES_DIR/70.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #71 ---
echo -n "Updating Issue #71... "
if gh issue edit 71 --repo "$REPO" --body-file "$ISSUES_DIR/71.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #72 ---
echo -n "Updating Issue #72... "
if gh issue edit 72 --repo "$REPO" --body-file "$ISSUES_DIR/72.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #73 ---
echo -n "Updating Issue #73... "
if gh issue edit 73 --repo "$REPO" --body-file "$ISSUES_DIR/73.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #74 ---
echo -n "Updating Issue #74... "
if gh issue edit 74 --repo "$REPO" --body-file "$ISSUES_DIR/74.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #75 ---
echo -n "Updating Issue #75... "
if gh issue edit 75 --repo "$REPO" --body-file "$ISSUES_DIR/75.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #76 ---
echo -n "Updating Issue #76... "
if gh issue edit 76 --repo "$REPO" --body-file "$ISSUES_DIR/76.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #77 ---
echo -n "Updating Issue #77... "
if gh issue edit 77 --repo "$REPO" --body-file "$ISSUES_DIR/77.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

# --- Issue #78 ---
echo -n "Updating Issue #78... "
if gh issue edit 78 --repo "$REPO" --body-file "$ISSUES_DIR/78.md" 2>/dev/null; then
    echo -e "${GREEN}✅${NC}"
    ((SUCCESS++))
else
    echo -e "${RED}❌ FAILED${NC}"
    ((FAIL++))
fi

echo ""
echo "================================================"
echo "완료: 성공 $SUCCESS / 실패 $FAIL"
echo "================================================"