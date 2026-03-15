# AI News Trend Analyzer

## Description
The AI News Trend Analyzer is a CLI tool that helps analyze the frequency and sentiment of AI-related topics in news articles over time. It is designed for AI developers and enthusiasts who want to track trending topics and understand the sentiment around them in the industry.

## Features
- Tracks keyword frequency in news articles over time.
- Performs sentiment analysis on news articles.
- Generates visual graphs for trend and sentiment analysis.

## Installation
1. Clone the repository or download the script `ai_news_trend_analyzer.py`.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script from the command line with the required arguments:

```bash
python ai_news_trend_analyzer.py --keywords 'GPT, LLM, AI ethics' --input news.csv
```

### Arguments
- `--keywords`: Comma-separated list of keywords to analyze (e.g., `GPT, LLM, AI ethics`).
- `--input`: Path to the input CSV file containing news articles. The CSV must have `timestamp` and `content` columns.

## Example Input File
The input CSV file should have the following structure:

| timestamp   | content                     |
|-------------|-----------------------------|
| 2023-10-01  | AI is transforming the world|
| 2023-10-02  | GPT models are advancing    |
| 2023-10-03  | AI ethics are critical      |

## Output
The tool generates graphs for each keyword showing:
1. Frequency of the keyword over time.
2. Average sentiment of articles containing the keyword over time.

## Testing
To run the tests, use:

```bash
pytest test_ai_news_trend_analyzer.py
```

The tests include scenarios for valid input, missing columns, and empty files.

## License
This project is licensed under the MIT License.
