import argparse
import feedparser
from transformers import pipeline
from bs4 import BeautifulSoup
import sys
import os

def fetch_rss_feed(url):
    try:
        feed = feedparser.parse(url)
        if feed.bozo:
            raise ValueError(f"Failed to parse feed: {feed.bozo_exception}")
        return feed.entries
    except Exception as e:
        print(f"Error fetching RSS feed: {e}", file=sys.stderr)
        return []

def summarize_text(text, summarizer, max_length):
    try:
        summary = summarizer(text, max_length=max_length, min_length=10, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        print(f"Error summarizing text: {e}", file=sys.stderr)
        return ""

def extract_text_from_entry(entry):
    try:
        if 'summary' in entry:
            return BeautifulSoup(entry['summary'], 'html.parser').get_text()
        elif 'content' in entry and entry['content']:
            return BeautifulSoup(entry['content'][0]['value'], 'html.parser').get_text()
        elif 'description' in entry:
            return BeautifulSoup(entry['description'], 'html.parser').get_text()
        else:
            return ""
    except Exception as e:
        print(f"Error extracting text from entry: {e}", file=sys.stderr)
        return ""

def main():
    parser = argparse.ArgumentParser(description="Real-Time News Summarizer")
    parser.add_argument('--category', type=str, help="Filter by category (optional)")
    parser.add_argument('--length', type=int, default=100, help="Maximum summary length (default: 100)")
    parser.add_argument('--source', type=str, nargs='+', required=True, help="RSS feed URLs to fetch news from")
    parser.add_argument('--output', type=str, help="File path to save the summaries (optional)")

    args = parser.parse_args()

    summarizer = pipeline("summarization")
    summaries = []

    for url in args.source:
        entries = fetch_rss_feed(url)
        for entry in entries:
            if args.category and args.category.lower() not in entry.get('tags', [{}])[0].get('term', '').lower():
                continue

            text = extract_text_from_entry(entry)
            if text:
                summary = summarize_text(text, summarizer, args.length)
                summaries.append({
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', 'No Link'),
                    'summary': summary
                })

    output = "\n\n".join([f"Title: {s['title']}\nLink: {s['link']}\nSummary: {s['summary']}" for s in summaries])

    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"Summaries saved to {args.output}")
        except Exception as e:
            print(f"Error writing to file: {e}", file=sys.stderr)
    else:
        print(output)

if __name__ == "__main__":
    main()
