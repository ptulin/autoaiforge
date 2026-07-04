# AI Code Audit

AI Code Audit leverages a pre-trained language model to analyze Python code for potential inefficiencies, unused imports, and common vulnerabilities such as unsafe input handling or poorly sanitized user data. This tool helps AI developers maintain cleaner, safer, and more performant codebases.

## Installation

Install the required dependencies using pip:

```bash
pip install rich openai
```

## Usage

Run the tool using the following command:

```bash
python ai_code_audit.py --path <path_to_file_or_directory>
```

Replace `<path_to_file_or_directory>` with the path to a Python file or a directory containing Python files.

## Features

- Analyze Python code for inefficiencies, unused imports, and security vulnerabilities.
- Generate actionable fixes and explanations.
- Display a detailed report in the terminal.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_audit.py
```

The tests mock external network calls to ensure they pass without requiring network access.
