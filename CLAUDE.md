# Daily AI Brief - 생성형 AI 뉴스레터 자동화 시스템

## 📋 프로젝트 개요

매일 아침 9시에 생성형 AI 관련 속보와 트렌드를 수집하여 HTML 뉴스레터 형태로 자동 생성하는 시스템입니다.

### 핵심 기능
- ⏰ **매일 아침 9시 자동 실행**
- 🔍 **생성형 AI 뉴스 수집** (ChatGPT, Claude, GPT-5, LLM 등)
- ✨ **아름다운 HTML 뉴스레터 생성**
- 💾 **날짜별 파일 저장** (최근 30일 유지)
- 🔗 **인덱스 페이지 자동 생성**

---

## 📁 프로젝트 구조

```
workspace/
├── config/
│   └── news_sources.json          # 뉴스 소스 및 검색 키워드 설정
├── scripts/
│   └── generate_brief.py          # 뉴스레터 생성 스크립트
├── daily_ai_brief/                # 생성된 뉴스레터 저장 폴더
│   ├── YYYY-MM-DD.html            # 날짜별 뉴스레터
│   └── index.html                 # 최신 뉴스레터 인덱스
└── CLAUDE.md                      # 이 파일
```

---

## 🚀 실행 방법

### 1. 수동 실행
```bash
python scripts/generate_brief.py
```

**결과:**
- `daily_ai_brief/{날짜}.html` - 오늘의 뉴스레터
- `daily_ai_brief/index.html` - 인덱스 페이지

브라우저에서 `daily_ai_brief/index.html` 또는 특정 날짜의 HTML 파일을 열어서 확인하세요.

### 2. 자동 실행 (매일 9시)
```bash
/schedule "python scripts/generate_brief.py" --cron "0 9 * * *" --repeat daily
```

또는 Claude Code의 schedule 스킬을 사용합니다.

---

## ⚙️ 설정 파일

### config/news_sources.json

**검색 키워드 (searchQueries)**
- 생성형 AI 관련 다양한 검색어 포함
- 예: "생성형 AI 뉴스", "ChatGPT 최신 뉴스", "Claude AI 발표" 등

**제외 키워드 (excludeKeywords)**
- 스팸, 광고, 채용공고, 주식 등 관계없는 기사 필터링

**뉴스 소스 신뢰도 (prioritySources)**
- 주요 언론사: 1.0 (한국일보, 중앙일보 등)
- 기술 미디어: 0.9~0.95 (테크크런치, 더버지 등)
- 블로그/유튜브: 0.5~0.6

**설정 옵션 (settings)**
- `maxArticlesPerDay`: 최대 기사 수 (기본 15개)
- `minWordCount`: 최소 단어 수 (기본 80)
- `language`: 언어 (한글)
- `timeRange`: 시간 범위 (24시간)

---

## 📊 생성되는 뉴스레터 구조

각 뉴스레터는 다음과 같이 구성됩니다:

1. **헤더**
   - 제목: Daily AI Brief
   - 부제: 생성형 AI 속보 & 트렌드
   - 날짜

2. **섹션별 뉴스**
   - 🔴 **속보** - 가장 긴급한 뉴스
   - 📰 **주요 뉴스** - 중요한 기사
   - 🚀 **기술 트렌드** - 기술 발전 소식
   - 💼 **산업뉴스** - 산업 관련 소식

3. **각 뉴스 항목**
   - 제목 (링크 포함)
   - 요약
   - 출처
   - 시간

4. **푸터**
   - 생성 일시
   - 자동화 정보

---

## 🔧 커스터마이징

### 검색 키워드 추가
`config/news_sources.json`의 `searchQueries` 배열에 추가:
```json
"searchQueries": [
  "생성형 AI 뉴스",
  "당신의_새로운_검색어"
]
```

### 최대 기사 수 변경
```json
"settings": {
  "maxArticlesPerDay": 20  // 기본값: 15
}
```

### 뉴스 소스 신뢰도 조정
`prioritySources` 객체에서 가중치를 조정합니다.
- 1.0: 최우선
- 0.5~0.95: 중간
- 0.3 이하: 낮음

---

## 🔄 자동화 설정

### Claude Code schedule 스킬 사용

1. **매일 9시 설정**
```bash
/schedule "python scripts/generate_brief.py" --repeat daily --time "09:00"
```

2. **매주 월~금 설정**
```bash
/schedule "python scripts/generate_brief.py" --cron "0 9 * * 1-5"
```

### 원격 실행 (클라우드)
schedule 스킬로 등록하면, Claude Code가 자동으로 매일 실행합니다.

---

## 📈 사용 시나리오

### 일일 업무 시작
1. 아침 9시에 자동으로 뉴스레터 생성
2. `daily_ai_brief/index.html` 열기
3. 최신 뉴스 확인
4. 팀에 공유

### 주간 리포트
```bash
# 최근 5일의 뉴스 확인
ls -lt daily_ai_brief/*.html | head -5
```

### 아카이브 관리
- 최근 30일 자동 유지
- 오래된 파일은 자동 정리 (향후 기능)

---

## 🐛 트러블슈팅

### Q: 스크립트가 실행되지 않음
**A:** Python이 설치되어 있는지 확인하세요.
```bash
python --version
```

### Q: 뉴스가 나오지 않음
**A:** 검색 쿼리를 확인하고 필요시 `config/news_sources.json` 수정

### Q: 자동화가 동작하지 않음
**A:** schedule 스킬이 제대로 등록되었는지 확인
```bash
/schedule list
```

---

## 📝 수정 이력

| 날짜 | 내용 |
|------|------|
| 2026-06-11 | 프로젝트 초기화 및 구조 구축 |
| - | schedule 스킬 자동화 설정 |

---

## 💡 향후 계획

- [ ] WebSearch API 통합 (실시간 뉴스 수집)
- [ ] 이메일 자동 발송 기능
- [ ] 클라우드 저장소 연동 (OneDrive, Google Drive)
- [ ] 뉴스 요약 AI 기능
- [ ] 한글/영문 자동 번역
- [ ] 구독자별 커스터마이징
- [ ] RSS 피드 생성

---

## 📧 문의 및 피드백

문제가 생기거나 개선사항이 있으면:
1. Python 스크립트의 에러 메시지 확인
2. `config/news_sources.json` 설정 검토
3. 수동 실행으로 문제 진단

---

**생성형 AI 속보를 놓치지 마세요!** 🤖
