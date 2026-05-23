import pytest
from unittest.mock import patch, Mock
from ai_news_analytics import analyze_sentiment, fetch_article_content, generate_sentiment_trend
import os

def test_analyze_sentiment():
    texts = ["AI is amazing and revolutionary!", "AI is dangerous and scary.", "AI is neutral."]
    sentiments, keyword_freq = analyze_sentiment(texts)

    assert len(sentiments) == 3
    assert all('compound' in sentiment for sentiment in sentiments)
    assert keyword_freq['ai'] == 3

def test_fetch_article_content():
    with patch('ai_news_analytics.requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "AI is transforming the world."
        mock_get.return_value = mock_response

        content = fetch_article_content("http://example.com")
        assert content == "AI is transforming the world."

        mock_get.assert_called_once_with("http://example.com", timeout=10)

def test_generate_sentiment_trend():
    sentiments = [
        {'compound': 0.5},
        {'compound': -0.2},
        {'compound': 0.1}
    ]
    output_file = "test_sentiment_trend.png"

    generate_sentiment_trend(sentiments, output_file)

    assert os.path.exists(output_file)
    os.remove(output_file)