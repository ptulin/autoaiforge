# Claude Code Assistant

Claude Code Assistant is a Python library designed to enhance coding workflows by leveraging Claude AI's capabilities. It integrates with Claude's API to suggest code snippets, debug issues, and refactor code based on user input.

## Features

- **Code Suggestion**: Generate code snippets based on a prompt.
- **Code Debugging**: Provide debugging insights for Python code.
- **Code Refactoring**: Optimize and refactor Python code.

## Installation

Install the required dependencies:

```bash
pip install requests pytest
```

## Usage

### CLI

Run the tool from the command line:

```bash
python claude_code_assistant.py --api_key YOUR_API_KEY --action suggest --input "Write a Python function to calculate Fibonacci."
```

### Library

Use the library in your Python code:

```python
from claude_code_assistant import ClaudeCodeAssistant

assistant = ClaudeCodeAssistant(api_key="YOUR_API_KEY")
result = assistant.suggest_code("Write a Python function to calculate Fibonacci.")
print(result)
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_code_assistant.py
```

## License

This project is licensed under the MIT License.