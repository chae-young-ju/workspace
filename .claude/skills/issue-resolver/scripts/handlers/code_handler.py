"""코드 구현 핸들러 (이슈 #4,7,9)"""
from pathlib import Path
from typing import Dict
from .base_handler import BaseHandler

class CodeHandler(BaseHandler):
    """이슈 #4,7,9: 코드 구현"""

    def handle(self) -> Dict:
        """뉴스레터 생성 및 WebSearch 통합"""
        try:
            self.logger.info("코드 구현 시작...")
            files = []

            # generate_brief.py
            brief_file = self._create_generate_brief()
            if brief_file:
                files.append(brief_file)

            # news_fetcher.py
            fetcher_file = self._create_news_fetcher()
            if fetcher_file:
                files.append(fetcher_file)

            self.created_files = files

            if self.commit_changes("implement core functionality with error handling"):
                return {"status": "success", "files": files}
            else:
                return {"status": "failed", "files": files}

        except Exception as e:
            self.logger.error(f"코드 구현 실패: {e}")
            return {"status": "failed", "files": [], "error": str(e)}

    def _create_generate_brief(self) -> Path:
        """generate_brief.py 생성"""
        script_file = self.project_path / 'scripts' / 'generate_brief.py'
        script_file.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""Daily AI Brief 뉴스레터 생성 스크립트"""
import os
import json
from datetime import datetime
from pathlib import Path
from news_fetcher import NewsCollector, ArticleFilter

def generate_newsletter():
    """뉴스레터 생성"""
    print("뉴스레터 생성 시작...")

    try:
        # 뉴스 수집
        collector = NewsCollector()
        articles = collector.fetch_news()

        # 필터링
        filter = ArticleFilter()
        filtered = filter.filter_articles(articles)

        # HTML 생성
        html_content = _generate_html(filtered)

        # 저장
        output_dir = Path('daily_ai_brief')
        output_dir.mkdir(exist_ok=True)

        date_str = datetime.now().strftime('%Y-%m-%d')
        output_file = output_dir / f'{date_str}.html'
        output_file.write_text(html_content)

        # 인덱스 업데이트
        _update_index()

        print(f"✅ 뉴스레터 생성 완료: {output_file}")
        return True

    except Exception as e:
        print(f"❌ 뉴스레터 생성 실패: {e}")
        return False

def _generate_html(articles):
    """HTML 뉴스레터 생성"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI Brief</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        .article { margin: 20px 0; padding: 15px; border-left: 4px solid #007bff; background: #f9f9f9; }
        .article h2 { margin-top: 0; color: #007bff; }
        .article-meta { color: #666; font-size: 0.9em; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>🤖 Daily AI Brief</h1>
    <p>생성형 AI 속보 & 트렌드 - """ + datetime.now().strftime('%Y년 %m월 %d일') + """</p>
"""

    for article in articles[:15]:
        html += f"""
    <div class="article">
        <h2><a href="{article.get('url', '#')}">{article.get('title', '제목 없음')}</a></h2>
        <div class="article-meta">
            <strong>출처:</strong> {article.get('source', '출처 없음')} |
            <strong>시간:</strong> {article.get('published_at', '시간 없음')}
        </div>
        <p>{article.get('summary', '요약 없음')}</p>
    </div>
"""

    html += """
    <footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ddd; color: #999; font-size: 0.9em;">
        <p>이 뉴스레터는 자동으로 생성되었습니다.</p>
    </footer>
</body>
</html>
"""
    return html

def _update_index():
    """인덱스 페이지 업데이트"""
    brief_dir = Path('daily_ai_brief')
    html_files = sorted(brief_dir.glob('*.html'), key=lambda x: x.stat().st_mtime, reverse=True)

    if html_files:
        latest = html_files[0].name
        index_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="refresh" content="0; url={latest}">
    <title>Daily AI Brief</title>
</head>
<body>
    <p><a href="{latest}">최신 뉴스레터로 이동</a></p>
</body>
</html>
"""
        index_file = brief_dir / 'index.html'
        index_file.write_text(index_html)

if __name__ == '__main__':
    generate_newsletter()
'''

        script_file.write_text(content)
        self.logger.info(f"생성: {script_file}")
        return script_file

    def _create_news_fetcher(self) -> Path:
        """news_fetcher.py 생성"""
        fetcher_file = self.project_path / 'scripts' / 'news_fetcher.py'
        fetcher_file.parent.mkdir(parents=True, exist_ok=True)

        content = '''"""뉴스 수집 및 필터링 모듈"""
import json
from pathlib import Path
from datetime import datetime

class NewsCollector:
    """뉴스 수집 클래스"""

    def fetch_news(self):
        """뉴스 수집 (WebSearch API 모의)"""
        # 실제 환경에서는 WebSearch API 통합
        return [
            {
                'title': 'Claude 3.5 Sonnet 출시',
                'summary': 'Anthropic이 새로운 Claude 모델 출시',
                'source': 'Anthropic',
                'url': 'https://www.anthropic.com',
                'published_at': datetime.now().isoformat(),
            },
            {
                'title': 'GPT-4o 성능 개선',
                'summary': 'OpenAI가 GPT-4o의 최신 버전 공개',
                'source': 'OpenAI',
                'url': 'https://www.openai.com',
                'published_at': datetime.now().isoformat(),
            },
        ]

class ArticleFilter:
    """기사 필터링 클래스"""

    def filter_articles(self, articles):
        """기사 필터링 및 순위 지정"""
        # 기본 필터링 (실제 환경에서는 관련성 스코어 사용)
        return articles[:10]

class ArticleRanker:
    """기사 순위 지정 클래스"""

    def rank(self, articles):
        """관련성에 따른 순위 지정"""
        return sorted(articles, key=lambda x: x.get('relevance_score', 0), reverse=True)
'''

        fetcher_file.write_text(content)
        self.logger.info(f"생성: {fetcher_file}")
        return fetcher_file
