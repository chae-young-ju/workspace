#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Daily AI Brief Generator
생성형 AI 뉴스레터 자동 생성 스크립트
"""

import json
import os
from datetime import datetime
from pathlib import Path

def load_config():
    """설정 파일 로드"""
    config_path = Path(__file__).parent.parent / "config" / "news_sources.json"
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_sample_articles():
    """
    샘플 기사 생성 (실제 환경에서는 WebSearch API 사용)
    현재는 데모용 데이터 제공
    """
    articles = [
        {
            "title": "OpenAI, GPT-4 Turbo 새 버전 출시",
            "summary": "OpenAI가 향상된 GPT-4 Turbo 모델을 발표했습니다. 더 빠른 속도와 개선된 정확도가 특징입니다.",
            "source": "테크크런치",
            "url": "https://techcrunch.com/",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "속보"
        },
        {
            "title": "Google DeepMind, 새로운 AI 모델 공개",
            "summary": "구글의 AI 연구팀이 혁신적인 언어모델을 발표했습니다. 멀티모달 기능이 강화되었습니다.",
            "source": "더버지",
            "url": "https://theverge.com/",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "주요 뉴스"
        },
        {
            "title": "Claude 3 API 성능 개선 소식",
            "summary": "Anthropic이 Claude 3 API의 성능을 대폭 개선했습니다. 응답 속도와 정확도가 향상되었습니다.",
            "source": "포브스",
            "url": "https://forbes.com/",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "기술 트렌드"
        },
        {
            "title": "생성형 AI 규제, 주요국 합의 추진",
            "summary": "G7 국가들이 AI 안전성 기준에 대한 합의를 진행하고 있습니다.",
            "source": "BBC",
            "url": "https://bbc.com/",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "주요 뉴스"
        },
        {
            "title": "AI 스타트업, $500M 펀딩 완료",
            "summary": "생성형 AI 관련 스타트업이 대규모 투자를 유치했습니다.",
            "source": "CNBC",
            "url": "https://cnbc.com/",
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "category": "산업뉴스"
        }
    ]
    return articles

def generate_html(articles, config):
    """HTML 뉴스레터 생성"""
    today = datetime.now()
    date_str = today.strftime("%Y년 %m월 %d일")
    file_date_str = today.strftime("%Y-%m-%d")

    # 카테고리별 분류
    by_category = {}
    for article in articles:
        category = article.get('category', '기타')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(article)

    # HTML 헤더
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI Brief - {date_str}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
        }}

        .container {{
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            overflow: hidden;
        }}

        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
        }}

        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}

        .date {{
            margin-top: 10px;
            font-size: 0.95em;
            opacity: 0.8;
        }}

        .content {{
            padding: 40px 30px;
        }}

        .section {{
            margin-bottom: 40px;
        }}

        .section-title {{
            font-size: 1.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
        }}

        .article {{
            margin-bottom: 25px;
            padding: 20px;
            background: #f8f9fa;
            border-left: 4px solid #667eea;
            border-radius: 4px;
            transition: all 0.3s ease;
        }}

        .article:hover {{
            background: #e8ebff;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
        }}

        .article-title {{
            font-size: 1.2em;
            font-weight: 700;
            color: #222;
            margin-bottom: 8px;
        }}

        .article-title a {{
            color: #667eea;
            text-decoration: none;
        }}

        .article-title a:hover {{
            text-decoration: underline;
        }}

        .article-summary {{
            color: #555;
            font-size: 0.95em;
            margin-bottom: 10px;
            line-height: 1.6;
        }}

        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.85em;
            color: #999;
        }}

        .source {{
            background: #e8ebff;
            color: #667eea;
            padding: 3px 8px;
            border-radius: 3px;
            font-weight: 500;
        }}

        .footer {{
            background: #f8f9fa;
            padding: 30px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
            border-top: 1px solid #e0e0e0;
        }}

        .footer p {{
            margin: 8px 0;
        }}

        @media (max-width: 600px) {{
            .header h1 {{
                font-size: 1.8em;
            }}

            .container {{
                margin: 0;
                border-radius: 0;
            }}

            .content {{
                padding: 20px 15px;
            }}

            .article {{
                padding: 15px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Daily AI Brief</h1>
            <p>생성형 AI 속보 & 트렌드</p>
            <div class="date">{date_str}</div>
        </div>

        <div class="content">
"""

    # 카테고리별 섹션 추가
    category_order = ['속보', '주요 뉴스', '기술 트렌드', '산업뉴스', '기타']

    for category in category_order:
        if category in by_category:
            articles_in_category = by_category[category]
            html += f'            <div class="section">\n'

            # 카테고리별 이모지
            emoji_map = {
                '속보': '🔴',
                '주요 뉴스': '📰',
                '기술 트렌드': '🚀',
                '산업뉴스': '💼',
                '기타': '📌'
            }
            emoji = emoji_map.get(category, '📌')

            html += f'                <h2 class="section-title">{emoji} {category}</h2>\n'

            for article in articles_in_category:
                html += f"""                <div class="article">
                    <div class="article-title">
                        <a href="{article['url']}" target="_blank">{article['title']}</a>
                    </div>
                    <div class="article-summary">{article['summary']}</div>
                    <div class="article-meta">
                        <span class="source">{article['source']}</span>
                        <span>{article['date']}</span>
                    </div>
                </div>
"""

            html += '            </div>\n'

    # HTML 푸터
    html += """        </div>

        <div class="footer">
            <p>📧 Daily AI Brief - 매일 아침 9시 자동 생성</p>
            <p>이 뉴스레터는 자동 생성되며, 생성형 AI 관련 속보를 중심으로 제공됩니다.</p>
            <p style="margin-top: 15px; font-size: 0.8em; color: #999;">
                최신 정보는 원본 출처를 참고하세요. |
                <a href="index.html" style="color: #667eea; text-decoration: none;">다른 뉴스레터</a>
            </p>
        </div>
    </div>
</body>
</html>
"""

    return html, file_date_str

def save_html(html, filename):
    """HTML 파일 저장"""
    output_dir = Path(__file__).parent.parent / "daily_ai_brief"
    output_dir.mkdir(parents=True, exist_ok=True)

    filepath = output_dir / f"{filename}.html"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return filepath

def create_index_html():
    """최신 뉴스레터 인덱스 생성"""
    output_dir = Path(__file__).parent.parent / "daily_ai_brief"
    index_path = output_dir / "index.html"

    # 최신 파일 찾기
    html_files = sorted(output_dir.glob("*.html"))
    html_files = [f for f in html_files if f.name != "index.html"]

    if not html_files:
        latest_file = None
        latest_date = "최신 뉴스레터 없음"
    else:
        latest_file = html_files[-1]
        latest_date = latest_file.stem

    # 인덱스 HTML 생성
    index_html = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily AI Brief - 뉴스레터</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0;
            padding: 20px;
        }
        .container {
            background: white;
            border-radius: 12px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
            padding: 50px;
            max-width: 600px;
            text-align: center;
        }
        h1 {
            color: #667eea;
            font-size: 2.5em;
            margin: 0 0 20px 0;
        }
        p {
            color: #666;
            font-size: 1.1em;
            margin: 15px 0;
        }
        .link-section {
            margin: 30px 0;
        }
        a {
            display: inline-block;
            margin: 10px;
            padding: 12px 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            transition: transform 0.2s ease;
        }
        a:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Daily AI Brief</h1>
        <p>생성형 AI 속보 & 트렌드 뉴스레터</p>
"""

    if latest_file:
        index_html += f"""
        <div class="link-section">
            <p>📰 <strong>최신 뉴스레터</strong></p>
            <a href="{latest_file.name}">📄 {latest_date} 뉴스레터 보기</a>
        </div>
"""

    # 최근 파일들 목록
    if html_files:
        index_html += """
        <div class="link-section">
            <p><strong>최근 뉴스레터</strong></p>
"""
        for html_file in sorted(html_files, reverse=True)[:10]:
            index_html += f'            <a href="{html_file.name}">{html_file.stem}</a><br>\n'

        index_html += "        </div>\n"

    index_html += """
        <p style="margin-top: 40px; font-size: 0.9em; color: #999;">
            매일 아침 9시에 자동 생성됩니다.
        </p>
    </div>
</body>
</html>
"""

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_html)

def main():
    """메인 함수"""
    print("🤖 Daily AI Brief Generator 시작...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 설정 로드
    config = load_config()
    print("✅ 설정 파일 로드 완료")

    # 샘플 기사 생성 (실제 환경에서는 WebSearch 사용)
    articles = generate_sample_articles()
    print(f"✅ {len(articles)}개 기사 수집 완료")

    # HTML 생성
    html, file_date = generate_html(articles, config)
    print("✅ HTML 생성 완료")

    # 파일 저장
    filepath = save_html(html, file_date)
    print(f"✅ 파일 저장: {filepath}")

    # 인덱스 생성
    create_index_html()
    print("✅ 인덱스 생성 완료")

    print("\n📧 Daily AI Brief 생성이 완료되었습니다!")
    print(f"📁 저장 위치: {filepath.parent}")

if __name__ == "__main__":
    main()
