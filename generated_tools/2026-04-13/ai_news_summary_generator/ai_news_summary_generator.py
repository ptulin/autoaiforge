import argparse
import json
import requests
from bs4 import BeautifulSoup
from transformers import pipeline

def fetch_articles(urls):
    """Fetches the content of articles from the given URLs."""
    articles = []
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract text content from the article
            paragraphs = soup.find_all('p')
            content = ' '.join(p.get_text() for p in paragraphs)
            articles.append({'url': url, 'content': content})
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
    return articles

def summarize_articles(articles, summarizer):
    """Summarizes the content of the articles using a summarization model."""
    summaries = []
    for article in articles:
        try:
            summary = summarizer(article['content'], max_length=130, min_length=30, do_sample=False)
            summaries.append({'url': article['url'], 'summary': summary[0]['summary_text']})
        except Exception as e:
            print(f"Error summarizing article from {article['url']}: {e}")
    return summaries

def save_summaries(summaries, output_file, output_format):
    """Saves the summaries to a file in the specified format."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            if output_format == 'json':
                json.dump(summaries, f, indent=4)
            else:
                for summary in summaries:
                    f.write(f"URL: {summary['url']}\n")
                    f.write(f"Summary: {summary['summary']}\n\n")
    except Exception as e:
        print(f"Error saving summaries: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI News Summary Generator")
    parser.add_argument('--urls', nargs='+', help="List of article URLs to summarize", required=True)
    parser.add_argument('--output', help="Output file to save summaries", required=True)
    parser.add_argument('--format', choices=['text', 'json'], default='text', help="Output format (text or json)")
    args = parser.parse_args()

    # Load the summarization pipeline
    summarizer = pipeline('summarization')

    # Fetch articles
    articles = fetch_articles(args.urls)

    # Summarize articles
    summaries = summarize_articles(articles, summarizer)

    # Save summaries
    save_summaries(summaries, args.output, args.format)

if __name__ == "__main__":
    main()