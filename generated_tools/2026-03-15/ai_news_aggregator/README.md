# AI News Aggregator

## Description
The AI News Aggregator is a Python tool that fetches and aggregates trending AI-related news from multiple RSS feeds or news APIs. It organizes the news by topic and presents a summarized report in various formats (text, JSON, or Markdown). This tool is useful for AI developers and enthusiasts to stay updated on the latest developments in AI without manually browsing multiple sources.

## Features
- Fetch news from multiple RSS feeds.
- Summarize articles by extracting key sentences.
- Output news in text, JSON, or Markdown format.

## Requirements
- Python 3.6+
- `feedparser`
- `beautifulsoup4`
- `nltk`

## Installation
Install the required Python packages using pip:

```bash
pip install feedparser beautifulsoup4 nltk
```

## Usage
Run the script with the following command:

```bash
python ai_news_aggregator.py --sources "<RSS_FEED_URL_1>,<RSS_FEED_URL_2>" --format <output_format>
```

### Arguments
- `--sources`: Comma-separated list of RSS feed URLs.
- `--format`: Output format (`text`, `json`, or `markdown`). Default is `text`.

### Example
```bash
python ai_news_aggregator.py --sources "http://example.com/rss,http://anotherexample.com/rss" --format markdown
```

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute:

```bash
pytest test_ai_news_aggregator.py
```

## License
This project is licensed under the MIT License.