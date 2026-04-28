import requests
import pandas as pd
from unittest.mock import MagicMock

class NewsPipeline:
    def __init__(self, api_keys):
        """
        Initialize the NewsPipeline with API keys.

        :param api_keys: Dictionary containing API keys for supported news APIs.
        """
        self.api_keys = api_keys
        self.summarizer = MagicMock()

    def fetch_news(self, topic, api="newsapi", page_size=10):
        """
        Fetch news articles based on a topic.

        :param topic: Topic to search for.
        :param api: API to use (default: 'newsapi').
        :param page_size: Number of articles to fetch (default: 10).
        :return: List of news articles.
        """
        if api == "newsapi":
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": topic,
                "pageSize": page_size,
                "apiKey": self.api_keys.get("newsapi")
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json().get("articles", [])
            else:
                response.raise_for_status()
        else:
            raise ValueError(f"Unsupported API: {api}")

    def clean_data(self, articles):
        """
        Clean and preprocess the fetched news articles.

        :param articles: List of raw news articles.
        :return: DataFrame of cleaned articles.
        """
        data = []
        for article in articles:
            data.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "content": article.get("content"),
                "url": article.get("url"),
                "publishedAt": article.get("publishedAt")
            })
        return pd.DataFrame(data)

    def summarize(self, text, max_length=50):
        """
        Summarize a given text using a pre-trained model.

        :param text: Text to summarize.
        :param max_length: Maximum length of the summary.
        :return: Summarized text.
        """
        if not text:
            return ""
        summaries = self.summarizer(text, max_length=max_length, min_length=10, do_sample=False)
        return summaries[0]["summary_text"] if summaries else ""

    def fetch_and_summarize(self, topic, api="newsapi", page_size=10):
        """
        Fetch, clean, and summarize news articles based on a topic.

        :param topic: Topic to search for.
        :param api: API to use (default: 'newsapi').
        :param page_size: Number of articles to fetch (default: 10).
        :return: List of summarized articles.
        """
        articles = self.fetch_news(topic, api, page_size)
        cleaned_data = self.clean_data(articles)
        cleaned_data["summary"] = cleaned_data["content"].apply(self.summarize)
        return cleaned_data.to_dict(orient="records")

if __name__ == "__main__":
    import argparse
    import json

    parser = argparse.ArgumentParser(description="News Data Pipeline")
    parser.add_argument("--api_key", required=True, help="API key for NewsAPI")
    parser.add_argument("--topic", required=True, help="Topic to fetch news for")
    parser.add_argument("--page_size", type=int, default=10, help="Number of articles to fetch")
    args = parser.parse_args()

    pipeline = NewsPipeline(api_keys={"newsapi": args.api_key})
    try:
        result = pipeline.fetch_and_summarize(topic=args.topic, page_size=args.page_size)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Error: {e}")