"""보안 및 환경 설정 핸들러 (이슈 #5-6)"""
from pathlib import Path
from typing import Dict
from .base_handler import BaseHandler

class SecurityHandler(BaseHandler):
    """이슈 #5-6: 보안 및 환경 설정 처리"""

    def handle(self) -> Dict:
        """환경 변수 및 보안 설정"""
        try:
            self.logger.info("보안 설정 시작...")
            files = []

            env_file = self._create_env_example()
            if env_file:
                files.append(env_file)

            gitignore_file = self._update_gitignore()
            if gitignore_file:
                files.append(gitignore_file)

            self.created_files = files

            if self.commit_changes("add security and environment configuration"):
                return {"status": "success", "files": files}
            else:
                return {"status": "failed", "files": files}

        except Exception as e:
            self.logger.error(f"보안 설정 실패: {e}")
            return {"status": "failed", "files": [], "error": str(e)}

    def _create_env_example(self) -> Path:
        """.env.example 생성"""
        env_file = self.project_path / '.env.example'
        content = """# GitHub 설정
GITHUB_TOKEN=your_github_token_here
GITHUB_REPO=chae-young-ju/workspace

# 프로젝트 설정
PROJECT_PATH=.
LOG_LEVEL=INFO

# API 키
NEWS_API_KEY=your_api_key_here

# 스케줄 설정
SCHEDULE_TIME=09:00
SCHEDULE_TIMEZONE=Asia/Seoul
"""
        env_file.write_text(content)
        self.logger.info(f"생성: {env_file}")
        return env_file

    def _update_gitignore(self) -> Path:
        """.gitignore 업데이트"""
        gitignore_file = self.project_path / '.gitignore'

        # 기존 내용 읽기 또는 새로 생성
        if gitignore_file.exists():
            content = gitignore_file.read_text()
        else:
            content = ""

        # .env 추가
        if ".env" not in content:
            content += "\n# Environment variables\n.env\n.env.local\n"

        # 기타 항목 추가
        ignores = [
            "__pycache__/",
            "*.py[cod]",
            "*$py.class",
            "*.so",
            ".Python",
            "build/",
            "develop-eggs/",
            "dist/",
            "downloads/",
            "eggs/",
            ".eggs/",
            "lib/",
            "lib64/",
            "parts/",
            "sdist/",
            "var/",
            "wheels/",
            "*.egg-info/",
            ".installed.cfg",
            "*.egg",
            ".venv",
            "venv/",
            "ENV/",
            "env/",
            "logs/",
            ".pytest_cache/",
            ".coverage",
            "htmlcov/",
            ".DS_Store",
        ]

        for ignore in ignores:
            if ignore not in content:
                content += f"{ignore}\n"

        gitignore_file.write_text(content)
        self.logger.info(f"업데이트: {gitignore_file}")
        return gitignore_file
