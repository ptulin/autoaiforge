# AI News Aggregator

## Overview
The AI News Aggregator is a Python tool that collects, aggregates, and categorizes the latest AI-related news from multiple online sources using RSS feeds. It allows developers to stay informed about the latest trends, breakthroughs, and discussions in AI.

## Features
- Fetches news from RSS feeds.
- Categorizes news based on user-defined categories.
- Exports categorized news to JSON or Markdown files.

## Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install feedparser
   ```

## Usage
Run the script with the following arguments:

```bash
python ai_news_aggregator.py --sources <path_to_sources_file> --categories <comma_separated_categories> --output <output_file>
```

### Arguments
- `--sources`: Path to a file containing RSS feed URLs (one URL per line).
- `--categories`: Comma-separated list of categories (e.g., `research,ethics`).
- `--output`: Output file path (e.g., `news.json` or `news.md`).

## Example
```bash
python ai_news_aggregator.py --sources sources.txt --categories research,ethics --output news.md
```

## Testing
Run the tests using pytest:
```bash
pytest test_ai_news_aggregator.py
```

## License
MIT License