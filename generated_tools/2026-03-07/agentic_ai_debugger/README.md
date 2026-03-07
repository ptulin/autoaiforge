# Agentic AI Debugger

Agentic AI Debugger is a CLI tool that integrates with IDEs to autonomously debug Python code. It uses OpenAI's API to analyze stack traces, error messages, and code context to suggest and apply fixes. This tool streamlines debugging by providing intelligent recommendations and fixes in real time.

## Features

- Analyze Python code and error messages using OpenAI's API.
- Suggest fixes and provide explanations for errors.
- Automatically apply fixes to code files.
- Process individual files or entire directories of Python scripts.

## Requirements

- Python 3.7+
- `openai` Python package
- `rich` Python package

## Installation

Install the required dependencies:

```bash
pip install openai rich
```

## Usage

Run the tool from the command line:

```bash
python agentic_ai_debugger.py --file <path_to_file> --error <error_message> --api-key <your_openai_api_key>
```

### Options

- `--file`: Path to a Python file to debug.
- `--directory`: Path to a directory containing Python files to debug.
- `--error`: Error message or stack trace to analyze (required).
- `--auto-apply`: Automatically apply suggested fixes.
- `--api-key`: Your OpenAI API key (required).

### Example

```bash
python agentic_ai_debugger.py --file example.py --error "ZeroDivisionError" --api-key YOUR_API_KEY --auto-apply
```

## Testing

To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_agentic_ai_debugger.py
```

The tests use mocking to simulate OpenAI API responses and file operations, so no actual API calls or file modifications are made during testing.
