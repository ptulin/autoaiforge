# Claude Apify Connector

## Overview
The Claude Apify Connector is a Python tool that facilitates seamless integration between Claude AI and the Apify platform. It simplifies the process of automating web scraping tasks using Apify and feeding the results into Claude for processing or analysis, enabling streamlined data collection and AI-powered insights.

## Features
- Fetch data from Apify using either an actor ID or a dataset ID.
- Send the fetched data to Claude AI for processing with a custom prompt.
- Command-line interface for easy usage.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_apify_connector
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the script using the command line:
```bash
python claude_apify_connector.py --api-key <APIFY_API_KEY> --openai-key <OPENAI_API_KEY> --prompt "Your prompt here" --actor-id <ACTOR_ID>
```

### Arguments
- `--api-key`: Your Apify API key (required).
- `--openai-key`: Your OpenAI API key for Claude (required).
- `--prompt`: The prompt to send to Claude AI (required).
- `--actor-id`: The Apify actor ID to run and fetch data from (optional if dataset ID is provided).
- `--dataset-id`: The Apify dataset ID to fetch data from (optional if actor ID is provided).

## Testing
To run the tests, install `pytest`:
```bash
pip install pytest
```
Then run:
```bash
pytest test_claude_apify_connector.py
```

## Requirements
- Python 3.7+
- `requests`

## Notes
- This tool uses mocked versions of the `ApifyClient` and `requests.post` for testing purposes. The actual `apify_client` package is not required for testing.
- Replace `<repository-url>` with the actual URL of the repository when cloning.
