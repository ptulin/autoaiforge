import argparse
import feedparser
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import sent_tokenize
import json

nltk.download('punkt')

def fetch_feed(url):
    """Fetch and parse the RSS feed from the given URL."""
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            raise ValueError(f"Failed to parse feed: {url}")
        return feed
    except Exception as e:
        raise ValueError(f"Error fetching feed {url}: {e}")

def summarize_text(text, max_sentences=3):
    """Summarize the given text by extracting the first few sentences."""
    sentences = sent_tokenize(text)
    return ' '.join(sentences[:max_sentences])

def extract_articles(feed):
    """Extract and summarize articles from the feed."""
    articles = []
    for entry in feed.entries:
        title = entry.get('title', 'No Title')
        link = entry.get('link', 'No Link')
        summary = entry.get('summary', '')
        # Clean HTML tags from the summary
        soup = BeautifulSoup(summary, 'html.parser')
        clean_summary = soup.get_text()
        summarized_text = summarize_text(clean_summary)
        articles.append({
            'title': title,
            'link': link,
            'summary': summarized_text
        })
    return articles

def aggregate_news(sources):
    """Aggregate news from multiple sources."""
    all_articles = []
    for source in sources:
        try:
            feed = fetch_feed(source)
            articles = extract_articles(feed)
            all_articles.extend(articles)
        except ValueError as e:
            print(e)
    return all_articles

def format_output(articles, output_format):
    """Format the aggregated articles into the specified format."""
    if output_format == 'json':
        return json.dumps(articles, indent=2)
    elif output_format == 'markdown':
        markdown_output = ""
        for article in articles:
            markdown_output += f"### {article['title']}\n\n{article['summary']}\n\n[Read more]({article['link']})\n\n"
        return markdown_output
    else:  # plain text
        text_output = ""
        for article in articles:
            text_output += f"Title: {article['title']}\nSummary: {article['summary']}\nLink: {article['link']}\n\n"
        return text_output

def main():
    parser = argparse.ArgumentParser(description="AI News Aggregator")
    parser.add_argument('--sources', required=True, help="Comma-separated list of RSS feed URLs.")
    parser.add_argument('--format', choices=['text', 'json', 'markdown'], default='text', help="Output format.")
    args = parser.parse_args()

    sources = args.sources.split(',')
    output_format = args.format

    articles = aggregate_news(sources)
    if not articles:
        print("No articles found.")
        return

    output = format_output(articles, output_format)
    print(output)

if __name__ == "__main__":
    main()