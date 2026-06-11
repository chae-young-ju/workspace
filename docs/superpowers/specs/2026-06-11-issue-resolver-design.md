# Issue Resolver 스킬 설계 문서

**작성일**: 2026-06-11  
**상태**: 승인됨  
**대상 프로젝트**: Daily AI Brief (workspace)

---

## 1. 개요

### 목적
생성된 11개의 GitHub 이슈를 자동으로 순차 처리하여 프로젝트를 완성시키는 스킬

### 핵심 기능
- 🔄 순차 처리: 각 이슈를 하나씩 처리 (추적 가능)
- 📝 자동 생성: 코드, 문서, 설정 파일 자동 생성
- ✅ 검증: 각 단계에서 생성 파일 검증
- 📌 자동 커밋: 각 이슈별로 git 커밋
- 📊 보고서: 최종 처리 결과 요약

---

## 2. 아키텍처

### 처리 흐름
```
시작 → 이슈 순회 → 핸들러 선택 → 파일 생성 → 검증 → Git 커밋 → 이슈 업데이트 → 다음 이슈
```

### 스킬 구조
```
issue-resolver/
├── SKILL.md                 # 스킬 설명
├── scripts/
│   ├── main.py             # 메인 오케스트레이션
│   ├── handlers/
│   │   ├── __init__.py
│   │   ├── doc_handler.py           # 이슈 #1-3 (문서화)
│   │   ├── security_handler.py      # 이슈 #5-6 (보안/환경)
│   │   ├── code_handler.py          # 이슈 #4,7,9 (코드)
│   │   ├── test_handler.py          # 이슈 #10 (테스트)
│   │   └── automation_handler.py    # 이슈 #8,11 (자동화)
│   └── utils/
│       ├── git_utils.py             # Git 커밋/푸시
│       ├── validation.py            # 파일 검증
│       └── logger.py                # 로깅
├── templates/               # 코드/문서 템플릿
└── evals/
    └── evals.json          # 테스트 케이스
```

---

## 3. 11개 이슈별 상세 처리 방식

### 이슈 #1: code-audit 스킬 Python 의존성 문서화

**입력**: .claude/skills/code-audit/ 경로  
**생성 파일**: `requirements.txt`  
**내용**: 
```
requests>=2.31.0
```

**처리**:
1. 기존 requirements.txt 확인
2. 필요한 의존성 목록 작성
3. 파일 생성
4. 커밋: `feat(#1): add code-audit skill requirements.txt`

---

### 이슈 #2: 종합적인 README.md 작성

**입력**: 프로젝트 구조, CLAUDE.md  
**생성 파일**: `README.md`  
**섹션**:
- 프로젝트 개요
- 주요 기능
- 설치 방법
- 사용 방법
- 프로젝트 구조
- 문제 해결
- 기여 방법

**처리**: AI 기반 markdown 생성

---

### 이슈 #3: code-audit 스킬 API 문서

**입력**: .claude/skills/code-audit/scripts/*.py  
**작업**: 기존 파일에 docstring 추가  
**대상 함수**:
- `CodeAnalyzer.analyze()`
- `CodeAnalyzer._analyze_file()`
- `CodeAnalyzer._analyze_python()`
- `IssueCreator.create_issue()`
- `IssueCreator.create_all_issues()`

**커밋**: `feat(#3): add comprehensive API documentation with docstrings`

---

### 이슈 #4: generate_brief.py 구현

**생성 파일**: `scripts/generate_brief.py`  
**주요 기능**:
1. `fetch_news()` - WebSearch API로 뉴스 수집
2. `filter_articles()` - 관련성 필터링
3. `generate_html()` - HTML 뉴스레터 생성
4. `save_newsletter()` - 파일 저장 및 인덱스 생성
5. `main()` - 메인 실행 로직

**처리**: 완전 동작하는 Python 코드 생성

---

### 이슈 #5: GitHub 토큰 보안

**생성 파일**: 
- `.env.example` (템플릿)
- 문서: CLAUDE.md 업데이트

**내용**:
```
GITHUB_TOKEN=your_token_here
NEWS_API_KEY=your_api_key_here
```

**처리**: .gitignore에 .env 추가, 문서 생성

---

### 이슈 #6: 환경 변수 관리

**생성 파일**: 
- `.env.example` (전체 템플릿)
- `.gitignore` (업데이트)

**환경 변수**:
- GITHUB_TOKEN
- PROJECT_PATH
- GITHUB_REPO
- API_KEYS 등

**처리**: 자동 생성 및 검증

---

### 이슈 #7: WebSearch API 통합

**생성 파일**: `scripts/news_fetcher.py`  
**주요 클래스**:
- `NewsCollector` - 뉴스 수집
- `ArticleFilter` - 필터링 로직
- `ArticleRanker` - 순위 지정

**API 통합**: Claude WebSearch를 통한 뉴스 수집  
**처리**: 완전 동작하는 코드 생성

---

### 이슈 #8: 뉴스레터 일일 스케줄 설정

**처리 방식**: 
1. /schedule 스킬 자동 호출
2. 설정: 매일 09:00 KST
3. 명령: `python scripts/generate_brief.py`

**커밋**: `feat(#8): setup daily newsletter generation schedule`

---

### 이슈 #9: 에러 처리 및 로깅

**수정 대상 파일**:
- `scripts/generate_brief.py` (자동 생성되므로 포함)
- `.claude/skills/code-audit/scripts/main.py`
- `.claude/skills/code-audit/scripts/create_issues.py`

**추가 기능**:
1. 구조화된 로깅 (logging 모듈)
2. 재시도 로직 (exponential backoff)
3. 에러 알림
4. 디버그 모드

**처리**: 기존 코드에 에러 처리 추가

---

### 이슈 #10: 단위 테스트 작성

**생성 파일**:
- `tests/test_generate_brief.py`
- `tests/test_news_fetcher.py`
- `tests/test_code_audit.py`
- `pytest.ini` 또는 `conftest.py`

**테스트 범위**:
- 뉴스 수집 기능
- 필터링/순위 로직
- HTML 생성
- 에러 처리

**처리**: pytest 기반 테스트 코드 자동 생성

---

### 이슈 #11: CI/CD 파이프라인

**생성 파일**: `.github/workflows/`
- `tests.yml` - 테스트 실행
- `lint.yml` - 코드 검사
- `scheduled.yml` - 정기적 실행

**GitHub Actions**:
1. PR/푸시 시 테스트 실행
2. 린트 검사 (pylint, flake8)
3. 타입 검사 (mypy)
4. 보안 스캔

**처리**: YAML 파일 자동 생성

---

## 4. 처리 순서 및 의존성

```
Phase 1 - 문서화 (이슈 #1-3)
  ↓
Phase 2 - 보안 & 설정 (이슈 #5-6)
  ↓
Phase 3 - 핵심 코드 (이슈 #4, #7, #9)
  ↓
Phase 4 - 완성 (이슈 #8, #10, #11)
```

### 의존성
- #4 (generate_brief.py)는 #5-6 (환경변수)에 의존
- #9 (에러 처리)는 #4 (코드) 생성 후 적용
- #8 (스케줄)은 #4 (코드) 완성 후 실행
- #10-11 (테스트/CI)는 모든 코드 생성 후

---

## 5. Git 커밋 전략

### 커밋 메시지 형식
```
feat(#{issue_number}): {description}

- 변경 사항 1
- 변경 사항 2
```

### 예시
```
feat(#1): add code-audit skill requirements.txt

- Create requirements.txt with dependency versions
- Document all Python dependencies for code-audit skill
```

### 커밋 순서
1. 이슈별 순차 커밋 (명확한 추적)
2. 각 커밋은 원자적 (한 이슈 = 한 커밋)
3. 최종: `docs: update project after issue resolution`

---

## 6. 검증 및 에러 처리

### 파일 검증 단계

**1단계: 구문 검사**
- Python: `ast.parse()` 또는 `compile()`
- JSON: `json.loads()`
- YAML: `yaml.safe_load()`
- Markdown: 기본 문법 검사

**2단계: 존재 확인**
- 파일이 실제로 생성됨
- 파일 크기 > 0
- 읽기 권한 확인

**3단계: 기본 로직 검증**
- Python: 핵심 함수/클래스 존재 확인
- 주요 import 확인

**4단계: Git 상태 확인**
- `git status` 로 파일 추가 확인
- 커밋 성공 여부

### 에러 처리

| 상황 | 처리 방식 | 재시도 |
|------|---------|--------|
| 파일 생성 실패 | 에러 로그 + 스킵 | X |
| 검증 실패 | 파일 삭제 후 재생성 | 최대 2회 |
| Git 커밋 실패 | 3회 재시도 후 중단 | 3회 |
| 의존성 에러 | 이후 이슈로 진행, 마지막에 보고 | N/A |

### 최종 보고서
```
✅ 완료된 이슈: #1-3, #5-11
❌ 실패한 이슈: #4 (사유: ...)
⚠️  부분 완료: 없음

생성된 파일: 15개
커밋된 파일: 15개
커밋 메시지: 11개
```

---

## 7. 구현 세부사항

### 주요 의존성
- `subprocess` - Git 명령 실행
- `pathlib.Path` - 파일 경로 관리
- `json`, `yaml` - 파일 검증
- `logging` - 로깅

### 설정 파일
- `config.json` - 이슈별 설정 (선택사항)
- `templates/` - 코드 템플릿

### 로깅
- 파일: `logs/issue_resolver.log`
- 레벨: INFO, ERROR, DEBUG
- 형식: `[timestamp] [level] [issue_#] message`

---

## 8. 성공 기준

✅ **모든 조건 충족 시 완료**
1. 11개 이슈 모두 처리됨
2. 각 파일 검증 성공
3. 각 커밋 성공
4. 최종 보고서 생성
5. 프로젝트 정상 동작 확인

---

## 9. 향후 고려사항

- 개별 이슈 재실행 기능 (특정 #만 다시 처리)
- 롤백 기능 (커밋 되돌리기)
- 병렬 처리 옵션 (순차 → 병렬 전환)
- 사용자 승인 게이트 (각 단계마다 확인)

---

**문서 상태**: 최종 승인 (2026-06-11)  
**다음 단계**: writing-plans 스킬로 구현 계획 수립
