# Code Review Bot

Code Review Bot is an automation tool that scans Python code files and provides LLM-powered reviews, highlighting potential issues, improvements, and compliance with coding standards. This tool is ideal for developers who want AI-assisted code reviews before pushing changes.

## Features

- Analyze Python code files for style and syntax issues using `flake8`.
- Get AI-powered feedback on code quality and best practices using OpenAI's API.
- Process individual files or entire directories containing Python files.
- Optionally save the review reports to text files.

## Requirements

- Python 3.7+
- `openai` Python package
- `flake8` Python package

Install the required packages using pip:

```bash
pip install openai flake8
```

## Usage

Run the tool from the command line:

```bash
python code_review_bot.py --path <file_or_directory_path> [--save]
```

### Arguments

- `--path`: Path to a Python file or directory containing Python files to review.
- `--save`: Optional flag to save the review report(s) to text file(s).

### Example

Review a single Python file:

```bash
python code_review_bot.py --path example.py
```

Review all Python files in a directory and save the reports:

```bash
python code_review_bot.py --path ./my_project --save
```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_code_review_bot.py
```

The tests include mocking for external dependencies like file I/O and network calls to ensure they run without requiring actual files or network access.
