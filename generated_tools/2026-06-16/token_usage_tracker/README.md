# Token Usage Tracker

## Overview
The Token Usage Tracker is a CLI tool that monitors token usage for AI model API calls. It helps developers track and optimize token consumption to reduce costs.

## Features
- Wraps API requests to an AI model and logs token usage.
- Generates reports in text or CSV format.

## Installation
1. Install Python 3.7 or higher.
2. Install the required dependencies:
   ```bash
   pip install requests click tabulate
   ```

## Usage
Run the tool from the command line:
```bash
python token_usage_tracker.py --api_key YOUR_API_KEY --model gpt-4 --output_format text
```

### Options
- `--api_key`: Your API key for the AI service (required).
- `--model`: The model to use (e.g., gpt-4) (required).
- `--output_format`: The format for the report (`text` or `csv`). Default is `text`.

### Example
```bash
python token_usage_tracker.py --api_key YOUR_API_KEY --model gpt-4 --output_format csv
```

Enter prompts one by one. Type `exit` to finish and generate the report.

## Testing
Run the tests using pytest:
```bash
pytest test_token_usage_tracker.py
```

All tests are mocked and do not require network access.