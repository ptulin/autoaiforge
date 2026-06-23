# Code Change Summarizer

Code Change Summarizer is a command-line tool that uses AI to generate human-readable summaries of code changes from the commit history of a GitHub repository. This tool is designed to help developers quickly understand what has changed and why, by summarizing commit diffs into concise explanations.

## Features

- Summarize code changes from commit diffs using OpenAI's language models.
- Support for filtering by file type or specific commit ranges.
- Generate reports in plain text or Markdown format for easy sharing.

## Installation

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool from the command line:

```bash
python code_change_summarizer.py --repo ./local_repo_path --range HEAD~5..HEAD --output changes.md --format markdown
```

### Arguments

- `--repo`: Path to the local Git repository.
- `--range`: Commit range to summarize (e.g., `HEAD~5..HEAD`).
- `--output`: Path to the output file where the summary will be saved.
- `--format`: Output format (`text` or `markdown`). Default is `text`.

## Example

```bash
python code_change_summarizer.py --repo ./my_repo --range HEAD~3..HEAD --output summary.txt --format text
```

This will generate a plain text summary of the last 3 commits and save it to `summary.txt`.

## Requirements

- Python 3.7+
- GitPython
- OpenAI Python SDK

## License

This project is licensed under the MIT License.