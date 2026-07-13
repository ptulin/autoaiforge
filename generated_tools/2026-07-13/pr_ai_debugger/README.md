# Pull Request AI Debugger

## Overview

`pr_ai_debugger` is a Python library designed to integrate AI-driven debugging directly into CI/CD pipelines. It scans pull requests for potential bugs, generates detailed diagnostic explanations, and suggests patches for common coding errors.

## Installation

Install the required dependencies using pip:

```bash
pip install openai requests pytest
```

## Usage

Run the tool from the command line:

```bash
python pr_ai_debugger.py --pr_id <pull_request_id> --repo <user/repo> --api_key <openai_api_key>
```

### Arguments
- `--pr_id`: The ID of the pull request to analyze.
- `--repo`: The repository name in the format `user/repo`.
- `--api_key`: Your OpenAI API key.

### Example

```bash
python pr_ai_debugger.py --pr_id 123 --repo user/repo --api_key YOUR_API_KEY
```

## Testing

Run the tests using pytest:

```bash
pytest test_pr_ai_debugger.py
```

The tests mock external network calls to ensure they pass without requiring actual API access.

## License

This project is licensed under the MIT License.