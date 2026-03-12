# Contextual Code Completer

## Overview

Contextual Code Completer is a Python tool that provides context-aware code generation by analyzing a project's existing codebase. It integrates with OpenAI's API to offer intelligent completion, refactoring suggestions, and boilerplate generation based on the existing context of the files.

## Features

- Analyze Python codebases to extract context.
- Generate code snippets based on queries and context.
- Handle edge cases such as empty directories and API errors.

## Installation

Install the required dependencies:

```bash
pip install openai
```

## Usage

Run the tool using the CLI:

```bash
python contextual_code_completer.py --path /path/to/codebase --query "Generate a new function"
```

## Testing

Run the tests using pytest:

```bash
pytest test_contextual_code_completer.py
```

## License

MIT License