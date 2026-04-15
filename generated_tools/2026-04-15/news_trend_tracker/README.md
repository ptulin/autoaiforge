# News Trend Tracker

## Overview
The News Trend Tracker is a Python tool that tracks emerging news trends by analyzing real-time updates across multiple RSS feed sources. It identifies common topics, clusters them, and generates concise summaries using AI-based summarization models. This tool is particularly useful for AI developers looking to create applications that adapt to dynamic, real-world information.

## Features
- Fetches and parses RSS feed entries.
- Clusters news articles into topics using KMeans clustering.
- Summarizes each cluster using a pre-trained summarization model.

## Requirements
- Python 3.7+
- Required Python packages:
  - `feedparser`
  - `scikit-learn`
  - `transformers`

Install the required packages using pip:
```bash
pip install feedparser scikit-learn transformers
```

## Usage
Run the script from the command line with the following arguments:

```bash
python news_trend_tracker.py --feeds <RSS_FEED_URL_1> <RSS_FEED_URL_2> ... --clusters <NUM_CLUSTERS> --summary_length <SUMMARY_LENGTH>
```

### Arguments
- `--feeds`: List of RSS feed URLs to analyze (required).
- `--clusters`: Number of clusters to form (default: 5).
- `--summary_length`: Maximum length of the summary for each cluster (default: 50).

### Example
```bash
python news_trend_tracker.py --feeds https://example.com/rss https://another.com/rss --clusters 3 --summary_length 100
```

## Testing
The tool includes a comprehensive test suite using `pytest`. To run the tests, install `pytest` and execute:

```bash
pip install pytest
pytest test_news_trend_tracker.py
```

The tests include mocking for external network calls to ensure they run without requiring internet access.

## License
This project is licensed under the MIT License.