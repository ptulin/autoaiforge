# News Sentiment Trader

## Overview
The News Sentiment Trader is a Python-based tool that analyzes news headlines and articles for sentiment related to specific stocks or cryptocurrencies. Based on the sentiment trends, it generates buy/sell/hold recommendations and integrates with popular trading platforms to automate trades.

## Features
- Fetches news articles from specified sources.
- Analyzes sentiment using the NLTK SentimentIntensityAnalyzer.
- Generates trading signals (buy/sell/hold) based on sentiment thresholds.
- Integrates with trading platforms via the CCXT library to execute trades.

## Requirements
- Python 3.7+
- `nltk`
- `ccxt`

## Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the NLTK `vader_lexicon`:
   ```python
   import nltk
   nltk.download('vader_lexicon')
   ```

## Usage
1. Create a configuration JSON file with the following structure:
   ```json
   {
       "assets": ["BTC/USD"],
       "news_sources": ["https://example.com/news"],
       "thresholds": {"buy": 0.5, "sell": -0.5},
       "trading_platform": {
           "exchange": "binance",
           "api_key": "your_api_key",
           "secret": "your_secret_key"
       }
   }
   ```
2. Run the tool:
   ```bash
   python news_sentiment_trader.py --config path_to_your_config.json
   ```

## Testing
To run the tests, install `pytest` and execute the following command:
```bash
pytest test_news_sentiment_trader.py
```

## Notes
- Ensure that the `vader_lexicon` is downloaded before running the tool.
- The tool is designed to work with the CCXT library for trading platform integration. Ensure your exchange is supported by CCXT.
