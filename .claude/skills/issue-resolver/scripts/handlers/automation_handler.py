"""자동화 및 CI/CD 핸들러 (이슈 #8,11)"""
from pathlib import Path
from typing import Dict
from .base_handler import BaseHandler

class AutomationHandler(BaseHandler):
    """이슈 #8,11: 자동화 및 CI/CD 설정"""

    def handle(self) -> Dict:
        """자동화 및 CI/CD 설정"""
        try:
            self.logger.info("자동화 설정 시작...")
            files = []

            # GitHub Actions 워크플로우
            tests_yml = self._create_tests_workflow()
            if tests_yml:
                files.append(tests_yml)

            lint_yml = self._create_lint_workflow()
            if lint_yml:
                files.append(lint_yml)

            self.created_files = files

            if self.commit_changes("setup CI/CD and scheduling"):
                return {"status": "success", "files": files}
            else:
                return {"status": "failed", "files": files}

        except Exception as e:
            self.logger.error(f"자동화 설정 실패: {e}")
            return {"status": "failed", "files": [], "error": str(e)}

    def _create_tests_workflow(self) -> Path:
        """tests.yml 생성"""
        workflow_dir = self.project_path / '.github' / 'workflows'
        workflow_dir.mkdir(parents=True, exist_ok=True)

        tests_yml = workflow_dir / 'tests.yml'

        content = '''name: Tests

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.8", "3.9", "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov

    - name: Run tests
      run: |
        pytest tests/ -v --cov=.claude/skills/code-audit/scripts --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: false
'''

        tests_yml.write_text(content)
        self.logger.info(f"생성: {tests_yml}")
        return tests_yml

    def _create_lint_workflow(self) -> Path:
        """lint.yml 생성"""
        workflow_dir = self.project_path / '.github' / 'workflows'
        workflow_dir.mkdir(parents=True, exist_ok=True)

        lint_yml = workflow_dir / 'lint.yml'

        content = '''name: Lint

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pylint black isort

    - name: Lint with flake8
      run: |
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics

    - name: Format check with black
      run: |
        black --check . --exclude=venv

    - name: Import sort check with isort
      run: |
        isort --check-only . --skip=venv
'''

        lint_yml.write_text(content)
        self.logger.info(f"생성: {lint_yml}")
        return lint_yml
