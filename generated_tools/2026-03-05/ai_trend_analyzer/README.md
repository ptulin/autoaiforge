# AI Trend Analyzer

## Overview
The AI Trend Analyzer is a CLI tool that analyzes recent AI news articles to extract trending topics, common keywords, and sentiment. It assists developers in identifying hot topics and sentiment shifts in the AI landscape.

## Features
- Extracts keywords from articles using spaCy.
- Analyzes sentiment using NLTK's SentimentIntensityAnalyzer.
- Generates a word cloud from the extracted keywords.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai-trend-analyzer.git
   cd ai-trend-analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the spaCy language model:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

Run the tool with the following command:

```bash
python ai_trend_analyzer.py --input <path_to_input_json> --output <path_to_output_image>
```

- `--input`: Path to a JSON file containing an array of articles (strings).
- `--output`: Path to save the generated word cloud image.

## Example

Input JSON file (`articles.json`):
```json
[
  "AI is transforming the world.",
  "Machine learning is a subset of AI."
]
```

Run the tool:
```bash
python ai_trend_analyzer.py --input articles.json --output wordcloud.png
```

## Testing

Run the tests using pytest:
```bash
pytest test_ai_trend_analyzer.py
```

## License
MIT License