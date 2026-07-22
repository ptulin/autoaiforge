# Code Diff Documentation Updater

## Description
The Code Diff Documentation Updater is a Python tool that automates the process of updating code documentation. It analyzes Git diffs to identify changes, uses AI to generate concise explanations for those changes, and updates inline docstrings or external documentation files like `README.md`.

## Features
- Analyze Git diffs to identify changes between commits or branches.
- Use OpenAI's GPT model to generate concise explanations for code changes.
- Automatically update `README.md` or other documentation files with inferred descriptions.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python code_diff_doc_updater.py --repo-path ./my_repo --branch main --openai-api-key YOUR_API_KEY
```

### Arguments
- `--repo-path`: Path to the Git repository (required).
- `--branch`: Branch to analyze (optional).
- `--commit-hash`: Specific commit hash to analyze (optional).
- `--openai-api-key`: OpenAI API key for generating docstrings (required).

## Example

```bash
python code_diff_doc_updater.py --repo-path ./my_repo --branch main --openai-api-key sk-12345
```

## Requirements
- Python 3.7+
- `openai==0.27.0`
- `gitpython==3.1.36`
- `pyyaml==6.0`

## License
MIT License