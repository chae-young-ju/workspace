"""문서화 작업 핸들러 (이슈 #1-3)"""
from pathlib import Path
from typing import Dict
from .base_handler import BaseHandler

class DocHandler(BaseHandler):
    """이슈 #1-3: 문서화 작업 처리"""

    def handle(self) -> Dict:
        """문서화 작업 처리"""
        try:
            self.logger.info("문서화 작업 시작...")
            files = []

            req_file = self._create_requirements()
            if req_file:
                files.append(req_file)

            readme_file = self._create_readme()
            if readme_file:
                files.append(readme_file)

            doc_files = self._add_docstrings()
            files.extend(doc_files)

            self.created_files = files

            if self.commit_changes("add documentation files"):
                return {"status": "success", "files": files}
            else:
                return {"status": "failed", "files": files}

        except Exception as e:
            self.logger.error(f"문서화 처리 실패: {e}")
            return {"status": "failed", "files": [], "error": str(e)}

    def _create_requirements(self) -> Path:
        """requirements.txt 생성"""
        req_file = self.project_path / '.claude' / 'skills' / 'code-audit' / 'requirements.txt'
        req_file.parent.mkdir(parents=True, exist_ok=True)
        content = "requests>=2.31.0\n"
        req_file.write_text(content)
        self.logger.info(f"생성: {req_file}")
        return req_file

    def _create_readme(self) -> Path:
        """README.md 생성"""
        readme_file = self.project_path / 'README.md'
        content = """# Daily AI Brief - 생성형 AI 뉴스레터 자동화 시스템

매일 아침 생성형 AI 관련 속보와 트렌드를 자동으로 수집하여 HTML 뉴스레터로 제공합니다.

## 주요 기능

- ⏰ **매일 자동 실행** - 오전 9시에 자동으로 뉴스레터 생성
- 🔍 **생성형 AI 뉴스 수집** - ChatGPT, Claude, LLM 등 최신 뉴스
- ✨ **아름다운 HTML 뉴스레터** - 반응형 디자인
- 💾 **자동 저장** - 날짜별 파일 저장 및 인덱스 생성
- 🔗 **WebSearch API 통합** - 실시간 뉴스 수집

## 설치

### 사전 요구사항
- Python 3.8+
- Git
- GitHub CLI (`gh`)

### 설정 단계

```bash
git clone https://github.com/chae-young-ju/workspace.git
cd workspace
pip install -r requirements.txt
cp .env.example .env
```

## 사용 방법

### 수동 실행
```bash
python scripts/generate_brief.py
```

### 자동 실행 (매일 9시)
자동화는 `/schedule` 스킬로 설정됩니다.

## 프로젝트 구조

```
workspace/
├── scripts/
│   ├── generate_brief.py
│   └── news_fetcher.py
├── config/
│   └── news_sources.json
├── daily_ai_brief/
│   └── index.html
├── .env.example
├── .claude/
│   └── skills/
│       ├── code-audit/
│       └── issue-resolver/
└── tests/
```

## 문제 해결

### 뉴스가 수집되지 않음
1. `.env` 파일에서 API 키 확인
2. 인터넷 연결 확인
3. 로그 파일 확인: `logs/issue_resolver.log`

## 기여

이슈 또는 PR을 통해 기여할 수 있습니다.

## 라이선스

MIT
"""
        readme_file.write_text(content)
        self.logger.info(f"생성: {readme_file}")
        return readme_file

    def _add_docstrings(self) -> list:
        """code-audit 스킬에 docstring 추가"""
        files_modified = []

        analyzer_file = self.project_path / '.claude' / 'skills' / 'code-audit' / 'scripts' / 'analyze_code.py'
        if analyzer_file.exists():
            content = analyzer_file.read_text()
            if '"""' not in content[:200]:
                new_content = '"""코드 분석 모듈 - 프로젝트 파일을 스캔하여 버그, 보안 이슈, 개선점을 찾습니다."""\n' + content
                analyzer_file.write_text(new_content)
                files_modified.append(analyzer_file)

        creator_file = self.project_path / '.claude' / 'skills' / 'code-audit' / 'scripts' / 'create_issues.py'
        if creator_file.exists():
            content = creator_file.read_text()
            if '"""' not in content[:200]:
                new_content = '"""GitHub 이슈 생성 모듈 - 분석 결과를 GitHub 이슈로 자동 생성합니다."""\n' + content
                creator_file.write_text(new_content)
                files_modified.append(creator_file)

        return files_modified
