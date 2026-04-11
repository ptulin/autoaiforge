# AI Code Suggestion CLI

## Overview
The AI Code Suggestion CLI is a tool that provides AI-powered real-time code suggestions and snippets based on incomplete code or comments provided by the user. It is useful for developers who want quick assistance in generating boilerplate code, refactoring, or filling in missing logic without needing to integrate into an IDE.

## Features
- Generate code suggestions based on incomplete code snippets.
- Provide optional comments to guide the AI.
- Save generated code to a file or display it in the terminal.

## Installation

Install the required Python packages:

```bash
pip install click openai pytest
```

## Usage

Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY=your_api_key
```

Run the CLI tool:

```bash
python ai_code_suggestion_cli.py --language python --snippet "def factorial(n):" --comment "Write code to calculate factorial recursively"
```

Optional: Save the generated code to a file:

```bash
python ai_code_suggestion_cli.py --language python --snippet "def factorial(n):" --comment "Write code to calculate factorial recursively" --output output.py
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_suggestion_cli.py
```

## License
MIT License
