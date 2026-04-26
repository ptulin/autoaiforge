import pytest
from unittest.mock import patch, MagicMock
from news_sentiment_trading_bot import fetch_news, analyze_sentiment, execute_trades

def test_fetch_news():
    with patch('news_sentiment_trading_bot.NewsApiClient') as mock_newsapi:
        mock_instance = MagicMock()
        mock_instance.get_top_headlines.return_value = {
            'articles': [{'title': 'Stock market rises'}, {'title': 'Economy is booming'}]
        }
        mock_newsapi.return_value = mock_instance

        headlines = fetch_news('fake_api_key')
        assert headlines == ['Stock market rises', 'Economy is booming']

def test_analyze_sentiment():
    with patch('news_sentiment_trading_bot.pipeline') as mock_pipeline:
        mock_sentiment_analyzer = MagicMock()
        mock_sentiment_analyzer.return_value = [{'label': 'POSITIVE', 'score': 0.9}]
        mock_pipeline.return_value = mock_sentiment_analyzer

        sentiment_scores = analyze_sentiment(['Stock market rises'])
        assert sentiment_scores == [('Stock market rises', 0.9)]

def test_execute_trades():
    with patch('news_sentiment_trading_bot.REST') as mock_rest:
        mock_instance = MagicMock()
        mock_rest.return_value = mock_instance

        sentiment_scores = [('Stock market rises', 0.9), ('Economy is crashing', -0.6)]
        execute_trades('fake_api_key', 'fake_api_secret', 0.8, -0.5, sentiment_scores)

        mock_instance.submit_order.assert_any_call(symbol='AAPL', qty=1, side='buy', type='market', time_in_force='gtc')
        mock_instance.submit_order.assert_any_call(symbol='AAPL', qty=1, side='sell', type='market', time_in_force='gtc')
