---
name: issue-resolver
description: |
  Automatically resolve all 11 GitHub issues for Daily AI Brief project.
  Creates documentation, code, tests, and CI/CD configuration in sequence.
  Each issue processed with validation and auto-commit.
compatibility: GitHub CLI, Python 3.8+, git
---

# Issue Resolver Skill

Automatically processes 11 GitHub issues to complete the Daily AI Brief project.

## How It Works

1. **순차 처리**: 이슈를 하나씩 처리 (추적 가능)
2. **자동 생성**: 코드, 문서, 설정 자동 생성
3. **검증**: 각 단계에서 파일 검증
4. **자동 커밋**: 이슈별로 git 커밋
5. **보고서**: 최종 처리 결과 요약

## 사용 방법

스킬 실행:
```
/issue-resolver
```

## 처리 이슈

- #1-3: 문서화 작업
- #4: generate_brief.py 구현
- #5-6: 보안 및 환경 설정
- #7: WebSearch API 통합
- #8: 스케줄 설정
- #9: 에러 처리 및 로깅
- #10: 테스트 작성
- #11: CI/CD 파이프라인
