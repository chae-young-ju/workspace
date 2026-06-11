"""테스트 작성 핸들러 (이슈 #10)"""
from pathlib import Path
from typing import Dict
from .base_handler import BaseHandler

class TestHandler(BaseHandler):
    """이슈 #10: 테스트 작성"""

    def handle(self) -> Dict:
        """테스트 코드 생성"""
        try:
            self.logger.info("테스트 코드 작성 시작...")
            files = []

            # 테스트 파일 생성
            test_brief = self._create_test_generate_brief()
            if test_brief:
                files.append(test_brief)

            test_fetcher = self._create_test_news_fetcher()
            if test_fetcher:
                files.append(test_fetcher)

            pytest_ini = self._create_pytest_ini()
            if pytest_ini:
                files.append(pytest_ini)

            self.created_files = files

            if self.commit_changes("add comprehensive test suite"):
                return {"status": "success", "files": files}
            else:
                return {"status": "failed", "files": files}

        except Exception as e:
            self.logger.error(f"테스트 작성 실패: {e}")
            return {"status": "failed", "files": [], "error": str(e)}

    def _create_test_generate_brief(self) -> Path:
        """test_generate_brief.py 생성"""
        test_file = self.project_path / 'tests' / 'test_generate_brief.py'
        test_file.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""뉴스레터 생성 테스트"""
import sys
from pathlib import Path

# scripts 디렉토리를 경로에 추가
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

def test_generate_newsletter_structure():
    """뉴스레터 구조 테스트"""
    from generate_brief import _generate_html

    articles = [
        {
            'title': '테스트 기사',
            'summary': '테스트 요약',
            'source': '테스트 출처',
            'url': 'https://example.com',
            'published_at': '2024-01-01'
        }
    ]

    html = _generate_html(articles)

    assert '<html>' in html
    assert '테스트 기사' in html
    assert '<!DOCTYPE html>' in html

def test_news_collector():
    """뉴스 수집 테스트"""
    from news_fetcher import NewsCollector

    collector = NewsCollector()
    articles = collector.fetch_news()

    assert isinstance(articles, list)
    assert len(articles) > 0
    assert 'title' in articles[0]
    assert 'summary' in articles[0]

def test_article_filter():
    """기사 필터링 테스트"""
    from news_fetcher import ArticleFilter

    articles = [{'title': f'Article {i}'} for i in range(20)]
    filter = ArticleFilter()
    filtered = filter.filter_articles(articles)

    assert len(filtered) <= 10
'''

        test_file.write_text(content)
        self.logger.info(f"생성: {test_file}")
        return test_file

    def _create_test_news_fetcher(self) -> Path:
        """test_news_fetcher.py 생성"""
        test_file = self.project_path / 'tests' / 'test_news_fetcher.py'
        test_file.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""뉴스 수집 테스트"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

def test_news_collector_fetch():
    """뉴스 수집 기능 테스트"""
    from news_fetcher import NewsCollector

    collector = NewsCollector()
    articles = collector.fetch_news()

    assert articles is not None
    assert isinstance(articles, list)

def test_article_filter_reduces_count():
    """필터링이 기사 수를 줄이는지 테스트"""
    from news_fetcher import ArticleFilter

    articles = [{'title': f'Article {i}'} for i in range(20)]
    filter = ArticleFilter()
    filtered = filter.filter_articles(articles)

    assert len(filtered) <= len(articles)

def test_article_ranker():
    """기사 순위 지정 테스트"""
    from news_fetcher import ArticleRanker

    articles = [
        {'title': 'A', 'relevance_score': 10},
        {'title': 'B', 'relevance_score': 20},
        {'title': 'C', 'relevance_score': 15},
    ]

    ranker = ArticleRanker()
    ranked = ranker.rank(articles)

    assert ranked[0]['title'] == 'B'  # 최고 점수
'''

        test_file.write_text(content)
        self.logger.info(f"생성: {test_file}")
        return test_file

    def _create_pytest_ini(self) -> Path:
        """pytest.ini 생성"""
        pytest_ini = self.project_path / 'pytest.ini'

        content = '''[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short
'''

        pytest_ini.write_text(content)
        self.logger.info(f"생성: {pytest_ini}")
        return pytest_ini
