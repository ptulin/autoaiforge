import argparse
import requests
import openai
import os

def fetch_news(api_key, topic, region):
    """Fetch news articles from NewsAPI."""
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "q": topic,
        "country": region,
        "apiKey": api_key
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("articles", [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

def summarize_articles(articles, summary_length, openai_api_key):
    """Summarize a list of articles using OpenAI's GPT model."""
    openai.api_key = openai_api_key
    summaries = []
    for article in articles:
        content = article.get("title", "") + " " + article.get("description", "")
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize the following text in {summary_length} sentences:\n{content}",
                max_tokens=150
            )
            summaries.append(response.choices[0].text.strip())
        except openai.error.OpenAIError as e:
            print(f"Error summarizing article: {e}")
            summaries.append("Error summarizing this article.")
    return summaries

def save_to_file(summaries, output_file):
    """Save summaries to a file."""
    try:
        with open(output_file, "w") as f:
            for summary in summaries:
                f.write(summary + "\n\n")
        print(f"Summaries saved to {output_file}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main():
    parser = argparse.ArgumentParser(description="News Summarizer CLI")
    parser.add_argument("--news_api_key", required=True, help="API key for NewsAPI")
    parser.add_argument("--openai_api_key", required=True, help="API key for OpenAI")
    parser.add_argument("--topic", required=True, help="Topic to search for")
    parser.add_argument("--region", required=True, help="Region code (e.g., 'us', 'gb')")
    parser.add_argument("--summary_length", type=int, default=3, help="Number of sentences in the summary")
    parser.add_argument("--output_file", help="File to save summaries")

    args = parser.parse_args()

    articles = fetch_news(args.news_api_key, args.topic, args.region)
    if not articles:
        print("No articles found.")
        return

    summaries = summarize_articles(articles, args.summary_length, args.openai_api_key)

    for i, summary in enumerate(summaries, 1):
        print(f"Article {i} Summary:\n{summary}\n")

    if args.output_file:
        save_to_file(summaries, args.output_file)

if __name__ == "__main__":
    main()
