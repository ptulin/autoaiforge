# Smart Autocomplete Agent

## Description
The Smart Autocomplete Agent is a Python tool that provides intelligent autocomplete suggestions for IDEs. It analyzes the current code context and offers AI-driven suggestions for function calls, argument structures, and code snippets based on coding history and common patterns.

## Features
- Generates intelligent autocomplete suggestions based on code context.
- Provides suggestions in both text and JSON formats.
- Handles edge cases such as empty input and errors gracefully.

## Installation
No external dependencies are required. The tool uses Python's standard library.

## Usage
Run the tool using the command line:

```bash
python smart_autocomplete_agent.py --code "<code_snippet>" --cursor <cursor_position> [--output-format text|json]
```

### Arguments
- `--code`: The code snippet for analysis.
- `--cursor`: The cursor position in the code snippet.
- `--output-format`: The output format for suggestions (`text` or `json`). Defaults to `text`.

### Example
```bash
python smart_autocomplete_agent.py --code "import numpy as np\nnp." --cursor 17 --output-format json
```

## Testing
To run the tests, use `pytest`:

```bash
pytest test_smart_autocomplete_agent.py
```

The tests include:
- Valid input.
- Empty input.
- Error handling with mocked exceptions.

## License
MIT License