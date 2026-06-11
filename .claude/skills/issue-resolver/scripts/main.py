"""Issue Resolver 메인 오케스트레이션"""
from pathlib import Path
from datetime import datetime
from handlers import (
    DocHandler, SecurityHandler, CodeHandler,
    TestHandler, AutomationHandler
)
from utils.logger import setup_logger

class IssueResolver:
    """11개 이슈 순차 처리"""

    def __init__(self, project_path: Path, repo: str):
        self.project_path = Path(project_path)
        self.repo = repo
        self.logger = setup_logger("issue_resolver")
        self.results = {}

    def resolve_all(self) -> dict:
        """모든 이슈 해결"""
        self.logger.info("=" * 60)
        self.logger.info("Issue Resolver 시작")
        self.logger.info(f"프로젝트: {self.project_path}")
        self.logger.info(f"저장소: {self.repo}")
        self.logger.info("=" * 60)

        handlers = [
            (DocHandler(1, self.project_path, self.repo), "#1-3: 문서화"),
            (SecurityHandler(2, self.project_path, self.repo), "#5-6: 보안"),
            (CodeHandler(3, self.project_path, self.repo), "#4,7,9: 코드"),
            (TestHandler(4, self.project_path, self.repo), "#10: 테스트"),
            (AutomationHandler(5, self.project_path, self.repo), "#8,11: 자동화"),
        ]

        success_count = 0
        for handler, description in handlers:
            self.logger.info(f"처리 중: {description}")
            result = handler.handle()
            self.results[description] = result

            if result['status'] == 'success':
                success_count += 1
                self.logger.info(f"✅ 완료: {description}")
            else:
                self.logger.error(f"❌ 실패: {description}")

        return self._generate_report(success_count, len(handlers))

    def _generate_report(self, success_count, total_count) -> dict:
        """최종 보고서 생성"""
        self.logger.info("=" * 60)
        self.logger.info("Issue Resolver 완료")
        self.logger.info("=" * 60)
        self.logger.info(f"완료: {success_count}/{total_count}")

        for task, result in self.results.items():
            status = "✅" if result['status'] == 'success' else "❌"
            self.logger.info(f"{status} {task}")

        return {
            "status": "complete",
            "success_count": success_count,
            "total_count": total_count,
            "results": self.results,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == '__main__':
    import sys

    project_path = sys.argv[1] if len(sys.argv) > 1 else Path.cwd()
    repo = sys.argv[2] if len(sys.argv) > 2 else "chae-young-ju/workspace"

    resolver = IssueResolver(project_path, repo)
    report = resolver.resolve_all()

    print("\\n최종 보고서:")
    print(f"상태: {report['status']}")
    print(f"완료: {report['success_count']}/{report['total_count']}")
