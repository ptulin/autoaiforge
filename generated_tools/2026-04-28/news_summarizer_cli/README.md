# News Summarizer CLI

## Description
The News Summarizer CLI is a command-line tool that aggregates headlines and articles from NewsAPI and summarizes them using OpenAI's GPT model. This tool allows developers to fetch, filter, and summarize news by topic or region for faster consumption.

## Features
- Fetch news articles by topic and region using NewsAPI.
- Summarize articles using OpenAI's GPT model.
- Customizable summarization length.
- Save summarized news to a text file.

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool with the following command:
```bash
python news_summarizer_cli.py --news_api_key YOUR_NEWSAPI_KEY \
                              --openai_api_key YOUR_OPENAI_KEY \
                              --topic "technology" \
                              --region "us" \
                              --summary_length 3 \
                              --output_file summaries.txt
```

### Example
```bash
python news_summarizer_cli.py --news_api_key YOUR_NEWSAPI_KEY \
                              --openai_api_key YOUR_OPENAI_KEY \
                              --topic "sports" \
                              --region "gb" \
                              --summary_length 2
```

## Requirements
- Python 3.7+
- requests==2.31.0
- openai==0.27.8

## License
This project is licensed under the MIT License.
