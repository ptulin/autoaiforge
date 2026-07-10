# Code Sanitizer AI

## Overview

Code Sanitizer AI is a Python tool that detects potential vulnerabilities in source code and provides AI-generated sanitized versions of problematic code snippets. It helps developers save time by automating the resolution of common security issues.

## Features

- Analyze individual files or entire directories for vulnerabilities.
- Generate sanitized versions of code automatically using OpenAI's GPT-4.
- Command-line interface for easy usage.

## Installation

Install the required dependencies using pip:

```bash
pip install click openai diff-match-patch
```

## Usage

### Analyze a Single File

```bash
python code_sanitizer_ai.py --file path/to/file.py
```

### Analyze and Sanitize a Single File

```bash
python code_sanitizer_ai.py --file path/to/file.py --sanitize
```

### Analyze a Directory

```bash
python code_sanitizer_ai.py --directory path/to/directory
```

### Analyze and Sanitize a Directory

```bash
python code_sanitizer_ai.py --directory path/to/directory --sanitize
```

## Testing

Run the tests using pytest:

```bash
pytest test_code_sanitizer_ai.py
```

## License

This project is licensed under the MIT License.