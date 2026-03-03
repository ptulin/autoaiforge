# AI Code Reviewer

## Overview

`ai_code_reviewer` is a CLI tool that performs an AI-driven code review on Python files. It analyzes your code's structure, style, and logic, providing suggestions for improvements, potential bugs, and best practices. This is especially useful for solo developers or small teams to maintain code quality.

## Installation

Install the required dependencies:

```bash
pip install click rich
```

## Usage

Run the tool with one or more Python files:

```bash
python ai_code_reviewer.py --files file1.py file2.py
```

Optional flags:

- `--style`: Include style analysis in the review.
- `--logic`: Include logic analysis in the review.
- `--bugs`: Include bug detection in the review.
- `--output`: Save the review to a markdown file.

Example:

```bash
python ai_code_reviewer.py --files file1.py --output review.md
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_reviewer.py
```

## License

MIT License