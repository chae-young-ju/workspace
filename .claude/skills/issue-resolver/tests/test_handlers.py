"""핸들러 테스트"""
from pathlib import Path

def test_base_handler_creation():
    """BaseHandler 테스트"""
    from ..scripts.handlers.base_handler import BaseHandler

    class TestHandler(BaseHandler):
        def handle(self):
            return {"status": "test"}

    handler = TestHandler(
        issue_number=1,
        project_path=Path.cwd(),
        repo="test/repo"
    )

    assert handler.issue_number == 1
    assert handler.project_path == Path.cwd()
    assert handler.repo == "test/repo"

def test_handlers_import():
    """모든 핸들러 import 테스트"""
    from ..scripts.handlers import (
        BaseHandler, DocHandler, SecurityHandler,
        CodeHandler, TestHandler, AutomationHandler
    )

    assert all([
        BaseHandler, DocHandler, SecurityHandler,
        CodeHandler, TestHandler, AutomationHandler
    ])
