# Smart Code Review Bot

## Overview
The Smart Code Review Bot is a Python tool that integrates AI coding assistants to perform automated code reviews. It analyzes Python code files, identifies potential bugs, inefficiencies, and style issues, and provides actionable feedback. This tool is especially useful for teams without dedicated senior reviewers.

## Features
- Analyze individual Python files for issues.
- Review all Python files in a directory.
- Provide actionable feedback using OpenAI's GPT models.

## Installation
Install the required dependencies:
```bash
pip install openai pygments
```

## Usage
Run the tool from the command line:
```bash
python smart_code_review.py <path-to-file-or-directory> --api-key <your-openai-api-key>
```

### Arguments
- `path`: Path to a Python file or directory containing Python files.
- `--api-key`: Your OpenAI API key.

## Example
Review a single file:
```bash
python smart_code_review.py example.py --api-key YOUR_API_KEY
```

Review all Python files in a directory:
```bash
python smart_code_review.py ./my_project --api-key YOUR_API_KEY
```

## Testing
Run the tests using pytest:
```bash
pytest test_smart_code_review.py
```

## License
MIT License