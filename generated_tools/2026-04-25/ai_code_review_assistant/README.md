# AI Code Review Assistant

## Overview

The AI Code Review Assistant is a Python-based CLI tool that leverages OpenAI's GPT-4 model to provide detailed reviews of code snippets. It offers suggestions for optimization, error fixes, and improvements.

## Features

- Analyze code snippets or files using OpenAI's GPT-4 model.
- Specify the programming language of the code for tailored feedback.
- Save the AI-generated review to a JSON file.

## Requirements

- Python 3.7+
- `openai` Python package

Install the required package using pip:

```bash
pip install openai
```

## Usage

Run the script from the command line with the following options:

```bash
python ai_code_review_assistant.py --api-key YOUR_API_KEY --file path/to/code.py --language Python --save review.json
```

### Arguments

- `--file`: Path to the code file to review.
- `--code`: Code snippet to review (alternative to `--file`).
- `--save`: Path to save the review output as a JSON file.
- `--api-key`: Your OpenAI API key (required).
- `--language`: Programming language of the code (default: Python).

### Examples

1. Review a code snippet directly:

    ```bash
    python ai_code_review_assistant.py --api-key YOUR_API_KEY --code "print('Hello, world!')"
    ```

2. Review a code file and save the output:

    ```bash
    python ai_code_review_assistant.py --api-key YOUR_API_KEY --file example.py --save review.json
    ```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_review_assistant.py
```

The tests mock external API calls and file operations, so no actual network access or files are required.
