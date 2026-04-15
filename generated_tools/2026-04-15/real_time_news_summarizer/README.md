# Real-Time News Summarizer

## Overview
The Real-Time News Summarizer is a command-line tool that aggregates trending news articles from online sources and generates AI-powered summaries in real-time. This tool is perfect for developers looking to extract concise insights from large volumes of news data without manually processing articles.

## Features
- Fetch news articles from multiple RSS feed sources.
- Filter articles by category.
- Generate AI-powered summaries of articles using Hugging Face's Transformers library.
- Save summaries to a file or display them in the console.

## Requirements
- Python 3.7+
- `feedparser`
- `transformers`
- `beautifulsoup4`
- `pytest` (for testing)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/real_time_news_summarizer.git
   cd real_time_news_summarizer
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python real_time_news_summarizer.py --source <RSS_FEED_URL> [--category <CATEGORY>] [--length <SUMMARY_LENGTH>] [--output <OUTPUT_FILE>]
```

### Arguments
- `--source`: One or more RSS feed URLs to fetch news from (required).
- `--category`: Filter articles by category (optional).
- `--length`: Maximum summary length (default: 100).
- `--output`: File path to save the summaries (optional).

### Example
Fetch and summarize news articles from two RSS feeds, filter by the category "technology", and save the summaries to a file:
```bash
python real_time_news_summarizer.py --source https://example.com/rss1.xml https://example.com/rss2.xml --category technology --length 50 --output summaries.txt
```

## Testing
Run the tests using `pytest`:
```bash
pytest test_real_time_news_summarizer.py
```

The tests include:
- Verifying RSS feed fetching functionality.
- Testing the summarization function with mocked AI summarizer.
- Ensuring text extraction from various RSS entry formats works correctly.

## License
This project is licensed under the MIT License.
