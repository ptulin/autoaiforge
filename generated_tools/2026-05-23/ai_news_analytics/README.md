# AI News Analytics

AI News Analytics is a Python tool designed to analyze the sentiment of AI-related news articles. It helps identify industry trends and public perception by analyzing the emotional tone of AI-related media coverage.

## Features

- Fetch article content from URLs.
- Analyze sentiment using the NLTK SentimentIntensityAnalyzer.
- Generate a sentiment trend graph.
- Identify keyword frequency in the analyzed texts.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_news_analytics.git
   cd ai_news_analytics
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following options:

```bash
python ai_news_analytics.py --urls <list_of_urls> --texts <list_of_texts> --output <output_file>
```

- `--urls`: A list of URLs pointing to AI-related news articles.
- `--texts`: A list of raw article texts to analyze.
- `--output`: The file path to save the sentiment trend graph (default: `sentiment_trend.png`).

### Example

```bash
python ai_news_analytics.py --texts "AI is amazing!" "AI is scary." --output sentiment.png
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_ai_news_analytics.py
```

## Requirements

- Python 3.7+
- nltk
- pandas
- matplotlib
- requests

## License

This project is licensed under the MIT License.