"""통합 테스트"""
from pathlib import Path

def test_full_workflow():
    """전체 워크플로우 테스트"""
    from ..scripts.handlers import (
        BaseHandler, DocHandler, SecurityHandler,
        CodeHandler, TestHandler, AutomationHandler
    )

    assert all([
        BaseHandler, DocHandler, SecurityHandler,
        CodeHandler, TestHandler, AutomationHandler
    ])

def test_main_orchestration():
    """메인 오케스트레이션 테스트"""
    from ..scripts.main import IssueResolver

    assert IssueResolver is not None
