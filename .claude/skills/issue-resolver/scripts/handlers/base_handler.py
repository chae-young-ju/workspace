"""핸들러 기본 클래스"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List
from ..utils.logger import setup_logger
from ..utils.git_utils import GitUtils
from ..utils.validation import Validator

class BaseHandler(ABC):
    """모든 이슈 핸들러의 기본 클래스"""

    def __init__(self, issue_number: int, project_path: Path, repo: str):
        self.issue_number = issue_number
        self.project_path = Path(project_path)
        self.repo = repo
        self.logger = setup_logger(f"issue_{issue_number}")
        self.git = GitUtils(self.project_path)
        self.validator = Validator()
        self.created_files: List[Path] = []

    @abstractmethod
    def handle(self) -> Dict:
        """이슈 처리"""
        pass

    def commit_changes(self, message: str) -> bool:
        """생성된 파일들을 커밋"""
        if not self.created_files:
            self.logger.warning(f"이슈 #{self.issue_number}: 커밋할 파일 없음")
            return False

        commit_message = f"feat(#{self.issue_number}): {message}"

        for attempt in range(3):
            if self.git.commit(self.created_files, commit_message):
                self.logger.info(f"이슈 #{self.issue_number}: 커밋 성공")
                return True

            self.logger.warning(f"이슈 #{self.issue_number}: 커밋 재시도 {attempt + 1}/3")

        self.logger.error(f"이슈 #{self.issue_number}: 커밋 실패")
        return False

    def log_result(self, result: Dict):
        """처리 결과 로깅"""
        status = result.get('status', 'unknown')
        files = result.get('files', [])

        if status == 'success':
            self.logger.info(f"이슈 #{self.issue_number}: 완료 ({len(files)}개 파일)")
        else:
            self.logger.error(f"이슈 #{self.issue_number}: 실패")
