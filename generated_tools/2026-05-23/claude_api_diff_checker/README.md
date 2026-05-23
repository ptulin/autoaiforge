# Claude API Diff Checker

## Description

The Claude API Diff Checker is a Python utility that compares two versions of the Claude AI API documentation and highlights changes, such as added, removed, or modified endpoints and parameters. This tool is essential for developers to quickly adapt their applications to API updates.

## Features

- Compare two JSON files or URLs containing API documentation.
- Generate a diff report highlighting added, removed, or modified endpoints and parameters.
- Export the diff report in JSON or Markdown format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_api_diff_checker
   ```

2. Install the required dependencies:
   ```bash
   pip install requests jsondiff
   ```

## Usage

Run the tool using the following command:

```bash
python claude_api_diff_checker.py --old <path_or_url_to_old_api> --new <path_or_url_to_new_api> --format <json|markdown>
```

### Arguments

- `--old`: Path or URL to the old API documentation (JSON).
- `--new`: Path or URL to the new API documentation (JSON).
- `--format`: Output format for the diff report. Options are `json` or `markdown`. Default is `markdown`.

### Example

```bash
python claude_api_diff_checker.py --old old_api.json --new new_api.json --format markdown
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute the tests:

```bash
pytest test_claude_api_diff_checker.py
```

All tests should pass successfully.

## License

This project is licensed under the MIT License.