"""유틸리티 테스트"""
import logging
import subprocess
from pathlib import Path
import tempfile

def test_logger_setup():
    """로거 설정 테스트"""
    from ..scripts.utils.logger import setup_logger

    logger = setup_logger("test", level=logging.DEBUG)

    assert logger is not None
    assert logger.name == "test"
    assert len(logger.handlers) > 0

def test_git_commit():
    """Git 커밋 테스트"""
    from ..scripts.utils.git_utils import GitUtils

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        subprocess.run(['git', 'init'], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@test.com'],
                      cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.name', 'Test'],
                      cwd=tmpdir, check=True, capture_output=True)

        test_file = tmpdir / "test.txt"
        test_file.write_text("test")

        git_utils = GitUtils(tmpdir)
        result = git_utils.commit([test_file], "test: add test file")

        assert result is True

def test_validator_python():
    """Python 검증 테스트"""
    from ..scripts.utils.validation import Validator

    validator = Validator()

    assert validator.validate_python("def test():\\n    return 42") is True
    assert validator.validate_python("def test(\\n    return 42") is False

def test_validator_json():
    """JSON 검증 테스트"""
    from ..scripts.utils.validation import Validator

    validator = Validator()

    assert validator.validate_json('{"key": "value"}') is True
    assert validator.validate_json('{"key": "value"') is False
