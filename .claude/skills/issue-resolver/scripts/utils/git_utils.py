"""Git 작업 유틸리티"""
import subprocess
from pathlib import Path
from typing import List, Dict

class GitUtils:
    """Git 명령 실행 래퍼"""

    def __init__(self, repo_path: Path):
        self.repo_path = Path(repo_path)

    def commit(self, files: List[Path], message: str) -> bool:
        """파일을 스테이징하고 커밋"""
        try:
            for file in files:
                subprocess.run(
                    ['git', 'add', str(file)],
                    cwd=self.repo_path,
                    check=True,
                    capture_output=True
                )

            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False

    def get_status(self) -> Dict[str, List[str]]:
        """Git 상태 반환"""
        try:
            result = subprocess.run(
                ['git', 'status', '--porcelain'],
                cwd=self.repo_path,
                check=True,
                capture_output=True,
                text=True
            )

            modified = []
            untracked = []

            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                status = line[:2]
                file = line[3:]

                if status == '??':
                    untracked.append(file)
                else:
                    modified.append(file)

            return {'modified': modified, 'untracked': untracked}
        except subprocess.CalledProcessError:
            return {'modified': [], 'untracked': []}

    def push(self, branch: str = 'main') -> bool:
        """원격 저장소로 푸시"""
        try:
            subprocess.run(
                ['git', 'push', 'origin', branch],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError:
            return False
