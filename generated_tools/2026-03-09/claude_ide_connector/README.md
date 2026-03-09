# Claude IDE Connector

The Claude IDE Connector is a Python library that allows developers to integrate Claude AI's coding capabilities directly into their IDEs. It provides features such as inline code suggestions, error analysis, and real-time optimizations to help developers write better code faster.

## Features

- **Code Suggestions**: Get suggestions for improving your code.
- **Error Analysis**: Analyze your code for errors and optimization hints.
- **Inline Completion**: Get inline code completion suggestions based on the cursor position.

## Installation

Install the required dependencies using pip:

```bash
pip install requests jedi rich
```

## Usage

### CLI Usage

You can use the CLI to interact with the Claude API:

```bash
python claude_ide_connector.py <api_key> <code> [--analyze | --suggest | --complete <cursor_position>]
```

- `--analyze`: Analyze the code for errors and optimizations.
- `--suggest`: Get code suggestions.
- `--complete`: Get inline completion at the given cursor position.

### Example

```bash
python claude_ide_connector.py my_api_key "print('Hello World')" --analyze
```

### Library Usage

You can also use the library in your Python code:

```python
from claude_ide_connector import Client

client = Client(api_key="your_api_key")

# Get code suggestions
suggestions = client.get_suggestions("print('Hello World')")
print(suggestions)

# Analyze code
analysis = client.analyze_code("print('Hello World')")
print(analysis)

# Inline completion
completion = client.inline_completion("print('Hello", cursor_position=6)
print(completion)
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_ide_connector.py
```

## License

This project is licensed under the MIT License.