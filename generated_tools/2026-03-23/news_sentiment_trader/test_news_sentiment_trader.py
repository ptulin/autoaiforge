import pytest
from unittest.mock import patch, MagicMock
from news_sentiment_trader import NewsSentimentTrader
from nltk.sentiment import SentimentIntensityAnalyzer

@pytest.fixture
def mock_config():
    return {
        "assets": ["BTC/USD"],
        "news_sources": ["https://example.com/news"],
        "thresholds": {"buy": 0.5, "sell": -0.5},
        "trading_platform": {
            "exchange": "binance",
            "api_key": "test_api_key",
            "secret": "test_secret"
        }
    }

@patch("news_sentiment_trader.NewsSentimentTrader.fetch_news")
@patch("news_sentiment_trader.NewsSentimentTrader.analyze_sentiment")
@patch("news_sentiment_trader.NewsSentimentTrader.execute_trade")
@patch("news_sentiment_trader.NewsSentimentTrader.load_config")
def test_run(mock_load_config, mock_execute_trade, mock_analyze_sentiment, mock_fetch_news, mock_config):
    mock_load_config.return_value = mock_config
    mock_fetch_news.return_value = "Bitcoin is surging to new highs!"
    mock_analyze_sentiment.return_value = 0.7

    trader = NewsSentimentTrader(config_path="test_config.json")
    trader.run()

    mock_fetch_news.assert_called_once_with("https://example.com/news")
    mock_analyze_sentiment.assert_called_once_with("Bitcoin is surging to new highs!")
    mock_execute_trade.assert_called_once_with("buy", "BTC/USD")

@patch("news_sentiment_trader.NewsSentimentTrader.load_config")
@patch("nltk.sentiment.SentimentIntensityAnalyzer.polarity_scores")
def test_analyze_sentiment(mock_polarity_scores, mock_load_config, mock_config):
    mock_load_config.return_value = mock_config
    mock_polarity_scores.return_value = {"compound": 0.8}

    trader = NewsSentimentTrader(config_path="test_config.json")
    result = trader.analyze_sentiment("Positive news about Bitcoin.")
    assert result == 0.8
    mock_polarity_scores.assert_called_once_with("Positive news about Bitcoin.")

@patch("news_sentiment_trader.NewsSentimentTrader.load_config")
def test_fetch_news(mock_load_config, mock_config):
    mock_load_config.return_value = mock_config
    trader = NewsSentimentTrader(config_path="test_config.json")
    result = trader.fetch_news("https://example.com/news")
    assert result == "Sample news content about Bitcoin."
