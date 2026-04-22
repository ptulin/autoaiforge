# Codex Debug Assistant

Codex Debug Assistant is a Python tool that integrates OpenAI Codex into debugging workflows. Developers can provide error messages, stack traces, or problematic code snippets, and the tool suggests fixes, explanations, or relevant tests to diagnose issues effectively.

## Features
- Accepts error messages, stack traces, or code snippets as input.
- Queries OpenAI Codex to provide debugging suggestions, explanations, and test cases.
- Displays results in a user-friendly format using the `rich` library.

## Requirements
- Python 3.7+
- `openai` library
- `rich` library

Install the required dependencies using pip:

```bash
pip install openai rich
```

## Usage

Run the tool from the command line:

```bash
python codex_debug_assistant.py --input "<error_message_or_code_snippet>" --api_key "<your_openai_api_key>"
```

### Example

```bash
python codex_debug_assistant.py --input "TypeError: unsupported operand type(s)" --api_key "sk-xxxxxxxxxxxxxxxxxxxx"
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests using:

```bash
pytest test_codex_debug_assistant.py
```

The tests include mocking of the OpenAI API to ensure no network access is required.