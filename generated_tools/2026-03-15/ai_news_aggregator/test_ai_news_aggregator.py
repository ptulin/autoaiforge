import pytest
from unittest.mock import patch, MagicMock
from ai_news_aggregator import fetch_feed, extract_articles, aggregate_news, format_output

def test_fetch_feed():
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = MagicMock(bozo=False, entries=[])
        feed = fetch_feed('http://example.com/rss')
        assert feed.bozo == False

def test_extract_articles():
    mock_feed = MagicMock()
    mock_feed.entries = [
        {
            'title': 'AI News 1',
            'link': 'http://example.com/1',
            'summary': '<p>This is a summary of AI News 1.</p>'
        },
        {
            'title': 'AI News 2',
            'link': 'http://example.com/2',
            'summary': '<p>This is a summary of AI News 2.</p>'
        }
    ]
    articles = extract_articles(mock_feed)
    assert len(articles) == 2
    assert articles[0]['title'] == 'AI News 1'
    assert articles[0]['summary'] == 'This is a summary of AI News 1.'

def test_format_output():
    articles = [
        {
            'title': 'AI News 1',
            'link': 'http://example.com/1',
            'summary': 'This is a summary of AI News 1.'
        }
    ]
    text_output = format_output(articles, 'text')
    assert 'AI News 1' in text_output
    assert 'http://example.com/1' in text_output
    markdown_output = format_output(articles, 'markdown')
    assert '### AI News 1' in markdown_output
    json_output = format_output(articles, 'json')
    assert 'AI News 1' in json_output

def test_aggregate_news():
    with patch('ai_news_aggregator.fetch_feed') as mock_fetch_feed:
        mock_feed = MagicMock()
        mock_feed.entries = [
            {
                'title': 'AI News 1',
                'link': 'http://example.com/1',
                'summary': '<p>This is a summary of AI News 1.</p>'
            }
        ]
        mock_fetch_feed.return_value = mock_feed
        sources = ['http://example.com/rss']
        articles = aggregate_news(sources)
        assert len(articles) == 1
        assert articles[0]['title'] == 'AI News 1'
        assert articles[0]['summary'] == 'This is a summary of AI News 1.'