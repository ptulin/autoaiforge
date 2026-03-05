import pytest
from unittest.mock import patch, mock_open
from ai_news_aggregator import fetch_rss_feed, categorize_news, export_to_file

def test_fetch_rss_feed():
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = {'entries': [{'title': 'AI News', 'link': 'http://example.com', 'summary': 'AI is evolving'}], 'bozo': 0}
        entries = fetch_rss_feed('http://example.com/rss')
        assert len(entries) == 1
        assert entries[0]['title'] == 'AI News'

def test_categorize_news():
    entries = [
        {'title': 'AI Ethics', 'link': 'http://example.com/ethics', 'summary': 'Ethical AI is important'},
        {'title': 'AI Research', 'link': 'http://example.com/research', 'summary': 'New AI research published'}
    ]
    categories = ['ethics', 'research']
    categorized = categorize_news(entries, categories)
    assert len(categorized['ethics']) == 1
    assert len(categorized['research']) == 1

def test_export_to_file():
    data = {
        'ethics': [{'title': 'AI Ethics', 'link': 'http://example.com/ethics', 'summary': 'Ethical AI is important'}],
        'research': [{'title': 'AI Research', 'link': 'http://example.com/research', 'summary': 'New AI research published'}]
    }
    with patch('builtins.open', mock_open()) as mocked_file:
        export_to_file(data, 'news.md')
        mocked_file.assert_called_once_with('news.md', 'w')
        handle = mocked_file()
        handle.write.assert_any_call('## ethics\n\n')
        handle.write.assert_any_call('### AI Ethics\n\n')
        handle.write.assert_any_call('Ethical AI is important\n\n')
        handle.write.assert_any_call('[Read more](http://example.com/ethics)\n\n')
