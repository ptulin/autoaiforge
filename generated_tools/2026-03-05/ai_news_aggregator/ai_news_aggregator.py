import argparse
import feedparser
import json

def fetch_rss_feed(url):
    try:
        feed = feedparser.parse(url)
        if hasattr(feed, 'bozo') and feed.bozo:
            raise ValueError(f"Failed to parse RSS feed: {url}")
        return feed.get('entries', [])
    except Exception as e:
        print(f"Error fetching RSS feed from {url}: {e}")
        return []

def categorize_news(entries, categories):
    categorized = {category: [] for category in categories}
    for entry in entries:
        content = entry.get('summary', '') + ' ' + entry.get('title', '')
        for category in categories:
            if category.lower() in content.lower():
                categorized[category].append({
                    'title': entry.get('title', 'No Title'),
                    'link': entry.get('link', 'No Link'),
                    'summary': entry.get('summary', 'No Summary')
                })
    return categorized

def export_to_file(data, output_file):
    try:
        with open(output_file, 'w') as f:
            if output_file.endswith('.json'):
                json.dump(data, f, indent=4)
            elif output_file.endswith('.md'):
                for category, items in data.items():
                    f.write(f"## {category}\n\n")
                    for item in items:
                        f.write(f"### {item['title']}\n\n")
                        f.write(f"{item['summary']}\n\n")
                        f.write(f"[Read more]({item['link']})\n\n")
            else:
                raise ValueError("Unsupported file format. Use .json or .md.")
        print(f"Exported news to {output_file}")
    except Exception as e:
        print(f"Error exporting to file: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI News Aggregator")
    parser.add_argument('--sources', required=True, help="Path to a file containing RSS feed URLs")
    parser.add_argument('--categories', required=True, help="Comma-separated list of categories (e.g., research,ethics)")
    parser.add_argument('--output', required=True, help="Output file path (e.g., news.json or news.md)")
    args = parser.parse_args()

    try:
        with open(args.sources, 'r') as f:
            sources = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Sources file not found: {args.sources}")
        return

    categories = [cat.strip() for cat in args.categories.split(',')]
    all_entries = []

    for source in sources:
        all_entries.extend(fetch_rss_feed(source))

    categorized_news = categorize_news(all_entries, categories)
    export_to_file(categorized_news, args.output)

if __name__ == "__main__":
    main()
