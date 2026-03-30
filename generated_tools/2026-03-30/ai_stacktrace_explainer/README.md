# AI Stacktrace Explainer

## Overview

The AI Stacktrace Explainer is a Python-based tool that helps developers analyze stack traces from error logs. It uses OpenAI's GPT-4 model to generate detailed explanations for the cause of the error and provides suggestions for resolution. This tool is particularly useful for debugging unfamiliar codebases.

## Features

- Reads stack traces from a file or standard input.
- Uses OpenAI's GPT-4 model to explain the stack trace.
- Outputs the explanation to the console or saves it to a file.

## Requirements

- Python 3.7+
- `openai` package
- `pygments` package

Install the required packages using pip:

```bash
pip install openai pygments
```

## Usage

### Command-Line Arguments

- `--tracefile`: Path to a file containing the stack trace.
- `--output`: Optional path to save the explanation output.

### Examples

1. **Read stack trace from a file and print explanation to the console:**

   ```bash
   python ai_stacktrace_explainer.py --tracefile error_log.txt
   ```

2. **Read stack trace from a file and save explanation to a file:**

   ```bash
   python ai_stacktrace_explainer.py --tracefile error_log.txt --output explanation.txt
   ```

3. **Pipe a stack trace to the script and print explanation to the console:**

   ```bash
   cat error_log.txt | python ai_stacktrace_explainer.py
   ```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key is required to use the GPT-4 model. Set it as an environment variable before running the script.

## Testing

The tool includes a test suite using `pytest`. To run the tests, install `pytest` and execute:

```bash
pip install pytest
pytest test_ai_stacktrace_explainer.py
```

The tests include:

1. Verifying behavior when the stack trace file is not found.
2. Testing successful reading of a stack trace file.
3. Mocking the OpenAI API to test the explanation functionality without network access.

## License

This project is licensed under the MIT License.