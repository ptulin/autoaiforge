# AI News Summary Generator

## Description
The AI News Summary Generator is a command-line tool that fetches AI-related news articles from specified URLs or RSS feeds and generates concise summaries using state-of-the-art Natural Language Processing (NLP) techniques. This tool is designed to save developers and enthusiasts time by extracting essential information from lengthy articles.

## Features
- Fetches AI news articles from URLs or RSS feeds.
- Uses NLP summarization models to generate concise summaries.
- Exports summaries to text or JSON files for further use.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_news_summary_generator.git
   cd ai_news_summary_generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python ai_news_summary_generator.py --urls <list_of_urls> --output <output_file> --format <text|json>
```

### Example

```bash
python ai_news_summary_generator.py --urls https://news.ai/article1 https://news.ai/article2 --output summaries.json --format json
```

This will fetch the articles from the provided URLs, generate summaries, and save them in a JSON file named `summaries.json`.

## Requirements
- Python 3.8+
- `requests`
- `beautifulsoup4`
- `transformers`

## Testing

To run the tests, use:

```bash
pytest test_ai_news_summary_generator.py
```

## License
This project is licensed under the MIT License.