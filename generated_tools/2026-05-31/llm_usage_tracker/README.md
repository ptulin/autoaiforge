# LLM Usage Tracker

## Overview

The LLM Usage Tracker is a Python library that allows developers to track LLM API usage at a granular level by logging request metadata (e.g., token usage, timestamps, user IDs) to a local SQLite database or a remote PostgreSQL database. It generates detailed usage reports to help identify trends and optimize costs.

## Features

- Log API usage with metadata such as API key, tokens used, user ID, and timestamp.
- Store logs in a local SQLite database or a remote PostgreSQL database.
- Generate usage reports in CSV or table format.

## Installation

Install the required dependencies using pip:

```bash
pip install sqlalchemy pandas rich
```

## Usage

### CLI Usage

Run the script with the following options:

- Log usage:

  ```bash
  python llm_usage_tracker.py --log --api-key <API_KEY> --tokens-used <TOKENS_USED> --user-id <USER_ID>
  ```

- Generate a report:

  ```bash
  python llm_usage_tracker.py --report --output-format <csv|table> [--output-file <FILE_PATH>]
  ```

### Example

Log usage:

```bash
python llm_usage_tracker.py --log --api-key my_api_key --tokens-used 150 --user-id user123
```

Generate a CSV report:

```bash
python llm_usage_tracker.py --report --output-format csv --output-file report.csv
```

Generate a table report:

```bash
python llm_usage_tracker.py --report --output-format table
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_usage_tracker.py
```

## License

This project is licensed under the MIT License.