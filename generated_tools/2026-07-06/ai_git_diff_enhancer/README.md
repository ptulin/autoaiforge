# AI Git Diff Enhancer

## Overview

The AI Git Diff Enhancer is a command-line tool that enhances Git diffs by providing AI-generated explanations for code changes. This tool helps developers review pull requests more efficiently by offering insights, suggestions, and potential improvements for the code changes.

## Features

- Analyze Git diffs from a specific commit, branch comparison, or a provided diff file.
- Generate AI-based explanations for code changes using OpenAI's API.
- Save annotated diffs with explanations to a markdown file.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd ai_git_diff_enhancer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python ai_git_diff_enhancer.py --commit <commit_hash> --branch <branch_name> --diff-file <path_to_diff_file> --output <output_file>
```

### Options:

- `--commit`: Git commit hash to analyze.
- `--branch`: Git branch name to compare with HEAD.
- `--diff-file`: Path to a diff file.
- `--output`: Path to save the annotated diff as a markdown file.

### Example:

```bash
python ai_git_diff_enhancer.py --commit abc123 --output annotated_diff.md
```

This command will analyze the Git diff for the specified commit (`abc123`), generate an AI-based explanation, and save the annotated diff to `annotated_diff.md`.

## Testing

To run the tests, use `pytest`:

```bash
pytest test_ai_git_diff_enhancer.py
```

The tests include:

- Mocked tests for the OpenAI API to ensure no network dependency.
- Tests for reading diffs from files.
- Tests for handling invalid inputs.

## Requirements

- Python 3.7+
- `click`
- `gitpython`
- `openai`

Install the dependencies using the provided `requirements.txt` file.

## Notes

- Ensure you have a valid OpenAI API key set in your environment variables as `OPENAI_API_KEY`.
- This tool requires Git to be installed and accessible in your system's PATH.
