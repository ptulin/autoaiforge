import pytest
from unittest.mock import patch, MagicMock
from real_time_news_summarizer import fetch_rss_feed, summarize_text, extract_text_from_entry

def test_fetch_rss_feed():
    with patch('feedparser.parse') as mock_parse:
        mock_parse.return_value = MagicMock(entries=[{'title': 'Test Article'}], bozo=False)
        entries = fetch_rss_feed('http://example.com/rss')
        assert len(entries) == 1
        assert entries[0]['title'] == 'Test Article'

def test_summarize_text():
    mock_summarizer = MagicMock()
    mock_summarizer.return_value = [{'summary_text': 'This is a summary.'}]
    summary = summarize_text("This is a test article.", mock_summarizer, 50)
    assert summary == 'This is a summary.'

def test_extract_text_from_entry():
    entry = {'summary': '<p>This is a test summary.</p>'}
    text = extract_text_from_entry(entry)
    assert text == 'This is a test summary.'

    entry = {'content': [{'value': '<p>This is a test content.</p>'}]}
    text = extract_text_from_entry(entry)
    assert text == 'This is a test content.'

    entry = {'description': '<p>This is a test description.</p>'}
    text = extract_text_from_entry(entry)
    assert text == 'This is a test description.'

    entry = {}
    text = extract_text_from_entry(entry)
    assert text == ''
