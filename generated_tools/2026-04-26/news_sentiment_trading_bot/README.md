# News Sentiment Trading Bot

## Overview
The News Sentiment Trading Bot is a Python-based tool that automates trading decisions based on sentiment analysis of financial news headlines. It fetches the latest business news, evaluates the sentiment of each headline, and triggers buy or sell actions on the Alpaca trading platform based on predefined sentiment thresholds.

## Features
- Fetches the latest business news headlines using the News API.
- Analyzes the sentiment of each headline using Hugging Face's Transformers library.
- Executes buy or sell trades on the Alpaca trading platform based on sentiment scores.

## Requirements
- Python 3.7+
- `newsapi-python`
- `transformers`
- `alpaca-trade-api`
- `pandas`
- `pytest` (for running tests)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script with the following command-line arguments:

```bash
python news_sentiment_trading_bot.py \
    --news_api_key <YOUR_NEWS_API_KEY> \
    --alpaca_api_key <YOUR_ALPACA_API_KEY> \
    --alpaca_api_secret <YOUR_ALPACA_API_SECRET> \
    --buy_threshold <BUY_THRESHOLD> \
    --sell_threshold <SELL_THRESHOLD>
```

### Arguments
- `--news_api_key`: API key for the News API.
- `--alpaca_api_key`: API key for the Alpaca trading API.
- `--alpaca_api_secret`: API secret for the Alpaca trading API.
- `--buy_threshold`: Sentiment score threshold for executing buy orders.
- `--sell_threshold`: Sentiment score threshold for executing sell orders.

## Testing
To run the tests, use the following command:

```bash
pytest test_news_sentiment_trading_bot.py
```

The tests include:
- Mocked tests for fetching news headlines.
- Mocked tests for sentiment analysis.
- Mocked tests for executing trades.

## Notes
- This tool is for educational purposes only and should not be used for live trading without thorough testing and risk management.
- Ensure you have valid API keys for both the News API and Alpaca trading platform before running the tool.

## License
This project is licensed under the MIT License.
