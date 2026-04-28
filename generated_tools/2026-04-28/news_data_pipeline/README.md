# News Data Pipeline

The News Data Pipeline is a Python library that provides a pipeline for fetching, cleaning, and summarizing news data. It enables developers to integrate AI-powered content curation into their own applications by providing modular components for API access, preprocessing, and summarization.

## Features

- Fetch news articles from NewsAPI.
- Clean and preprocess fetched news articles.
- Summarize news content using a mock summarization pipeline.

## Installation

Install the required dependencies using pip:

```bash
pip install requests pandas
```

## Usage

Run the script from the command line:

```bash
python news_data_pipeline.py --api_key YOUR_NEWSAPI_KEY --topic "Artificial Intelligence" --page_size 5
```

Replace `YOUR_NEWSAPI_KEY` with your NewsAPI key and specify the topic you want to fetch news for.

## Testing

Run the tests using pytest:

```bash
pytest test_news_data_pipeline.py
```

All tests are mocked and do not require network access.

## Dependencies

- `requests`
- `pandas`

## License

This project is licensed under the MIT License.