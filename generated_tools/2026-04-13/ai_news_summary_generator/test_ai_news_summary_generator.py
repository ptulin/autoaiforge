import pytest
from unittest.mock import patch, Mock
from ai_news_summary_generator import fetch_articles, summarize_articles, save_summaries

def test_fetch_articles():
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "<html><body><p>Test content</p></body></html>"
    with patch('requests.get', return_value=mock_response):
        articles = fetch_articles(["http://example.com"])
        assert len(articles) == 1
        assert articles[0]['content'] == "Test content"

def test_summarize_articles():
    mock_summarizer = Mock()
    mock_summarizer.return_value = [{'summary_text': 'Summarized content'}]
    articles = [{'url': 'http://example.com', 'content': 'Long article content'}]
    summaries = summarize_articles(articles, mock_summarizer)
    assert len(summaries) == 1
    assert summaries[0]['summary'] == 'Summarized content'

def test_save_summaries(tmp_path):
    summaries = [{'url': 'http://example.com', 'summary': 'Summarized content'}]
    output_file = tmp_path / "output.txt"
    save_summaries(summaries, output_file, 'text')
    with open(output_file, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "http://example.com" in content
    assert "Summarized content" in content