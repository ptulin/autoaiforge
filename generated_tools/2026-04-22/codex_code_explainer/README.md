# Codex Code Explainer

Codex Code Explainer is a Python tool that uses OpenAI Codex to generate human-readable explanations for complex Python code. This tool is ideal for onboarding new developers, analyzing third-party scripts, or understanding obscure algorithms.

## Features
- Generate detailed explanations for Python code.
- Handle empty input gracefully.
- Provide error messages for API-related issues.

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies:

```bash
pip install openai pytest
```

## Usage

Run the script from the command line:

```bash
python codex_code_explainer.py "<your_python_code>"
```

Example:

```bash
python codex_code_explainer.py "def add(a, b):\n    return a + b"
```

## Testing

To run the tests, use pytest:

```bash
pytest test_codex_code_explainer.py
```

## Requirements

- Python 3.7+
- `openai` library
- `pytest` for testing

## License

This project is licensed under the MIT License.
