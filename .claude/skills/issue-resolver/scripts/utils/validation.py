"""파일 검증 유틸리티"""
import json
import ast
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

class Validator:
    """파일 검증 클래스"""

    @staticmethod
    def validate_python(code: str) -> bool:
        """Python 코드 검증"""
        try:
            ast.parse(code)
            return True
        except SyntaxError:
            return False

    @staticmethod
    def validate_json(content: str) -> bool:
        """JSON 검증"""
        try:
            json.loads(content)
            return True
        except json.JSONDecodeError:
            return False

    @staticmethod
    def validate_yaml(content: str) -> bool:
        """YAML 검증"""
        if not HAS_YAML:
            return True
        try:
            yaml.safe_load(content)
            return True
        except:
            return False

    @staticmethod
    def validate_markdown(content: str) -> bool:
        """Markdown 검증"""
        return len(content) > 0

    @staticmethod
    def file_exists(path: Path) -> bool:
        """파일 존재 확인"""
        return path.exists() and path.is_file()

    @staticmethod
    def file_not_empty(path: Path) -> bool:
        """파일 크기 확인"""
        return path.exists() and path.stat().st_size > 0
