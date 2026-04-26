import argparse
import logging
from newsapi import NewsApiClient
from transformers import pipeline
from alpaca_trade_api import REST
import pandas as pd

def fetch_news(api_key):
    try:
        newsapi = NewsApiClient(api_key=api_key)
        headlines = newsapi.get_top_headlines(category='business', language='en', page_size=10)
        articles = headlines.get('articles', [])
        return [article['title'] for article in articles]
    except Exception as e:
        logging.error(f"Error fetching news: {e}")
        return []

def analyze_sentiment(headlines):
    try:
        sentiment_analyzer = pipeline('sentiment-analysis')
        results = []
        for headline in headlines:
            sentiment = sentiment_analyzer(headline)[0]
            score = sentiment['score'] if sentiment['label'].upper() == 'POSITIVE' else -sentiment['score']
            results.append((headline, score))
        return results
    except Exception as e:
        logging.error(f"Error analyzing sentiment: {e}")
        return []

def execute_trades(api_key, api_secret, buy_threshold, sell_threshold, sentiment_scores):
    try:
        alpaca = REST(api_key, api_secret, base_url='https://paper-api.alpaca.markets')
        for headline, score in sentiment_scores:
            if score >= buy_threshold:
                alpaca.submit_order(symbol='AAPL', qty=1, side='buy', type='market', time_in_force='gtc')
                logging.info(f"Executed BUY order for AAPL based on headline: {headline}")
            elif score <= sell_threshold:
                alpaca.submit_order(symbol='AAPL', qty=1, side='sell', type='market', time_in_force='gtc')
                logging.info(f"Executed SELL order for AAPL based on headline: {headline}")
    except Exception as e:
        logging.error(f"Error executing trades: {e}")

def main():
    parser = argparse.ArgumentParser(description="News Sentiment Trading Bot")
    parser.add_argument('--news_api_key', required=True, help="API key for News API")
    parser.add_argument('--alpaca_api_key', required=True, help="API key for Alpaca trading API")
    parser.add_argument('--alpaca_api_secret', required=True, help="API secret for Alpaca trading API")
    parser.add_argument('--buy_threshold', type=float, required=True, help="Sentiment score threshold for buying")
    parser.add_argument('--sell_threshold', type=float, required=True, help="Sentiment score threshold for selling")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    headlines = fetch_news(args.news_api_key)
    if not headlines:
        logging.error("No headlines fetched. Exiting.")
        return

    sentiment_scores = analyze_sentiment(headlines)
    if not sentiment_scores:
        logging.error("No sentiment scores generated. Exiting.")
        return

    execute_trades(args.alpaca_api_key, args.alpaca_api_secret, args.buy_threshold, args.sell_threshold, sentiment_scores)

if __name__ == "__main__":
    main()
