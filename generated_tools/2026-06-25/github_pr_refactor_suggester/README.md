# GitHub PR Refactor Suggester

## Overview
This tool connects to GitHub, retrieves the diff of a pull request, and uses OpenAI's API to suggest refactor opportunities based on common design principles and patterns. It's ideal for teams aiming to enhance code quality and maintainability.

## Installation

Install the required Python packages:

```bash
pip install requests openai pytest
```

## Usage

Run the tool using the following command:

```bash
python github_pr_refactor_suggester.py --token <github_token> --repo <owner/repo> --pr <pull_request_id> --openai-key <openai_api_key> [--output <output_file>]
```

### Arguments

- `--token`: Your GitHub personal access token.
- `--repo`: The GitHub repository in the format `owner/repo`.
- `--pr`: The pull request ID.
- `--openai-key`: Your OpenAI API key.
- `--output`: (Optional) File path to save suggestions in markdown format.

## Testing

Run the tests using pytest:

```bash
pytest test_github_pr_refactor_suggester.py
```

The tests mock external network calls to ensure they pass without actual API access.

## License

This project is licensed under the MIT License.