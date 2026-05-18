# AI Snippet Suggester

## Overview
AI Snippet Suggester is a CLI tool that generates relevant code snippets for a given problem statement or function description using OpenAI APIs. This tool helps developers quickly bootstrap functionality or learn how to solve specific problems without leaving their terminal.

## Installation

1. Install Python 3.7 or higher.
2. Install the required package:

```bash
pip install openai
```

## Usage

Run the tool using the following command:

```bash
python ai_snippet_suggester.py --description "Sort a list of integers" --language "python"
```

### Options

- `--description`: Problem description or function idea (required).
- `--language`: Programming language for the snippet (required).
- `--temperature`: Sampling temperature for the model (default: 0.7).
- `--max_tokens`: Maximum tokens for the response (default: 150).
- `--output`: File path to save the generated snippet (optional).

### Example

```bash
python ai_snippet_suggester.py --description "Sort a list of integers" --language "python" --output snippet.py
```

This will generate a Python code snippet for sorting a list of integers and save it to `snippet.py`.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_snippet_suggester.py
```

All tests are mocked and do not require network access.

## License

This project is licensed under the MIT License.