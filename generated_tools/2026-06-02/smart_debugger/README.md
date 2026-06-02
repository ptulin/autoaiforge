# Smart Debugger

Smart Debugger is a Python tool that analyzes Python traceback errors and provides suggestions to fix the issue using LLM-based reasoning. This tool is useful for developers who want smarter debugging capabilities directly in their development environment.

## Features
- Analyze Python traceback strings.
- Get human-readable explanations and suggestions for fixing errors.

## Installation

Install the required dependencies:

```bash
pip install openai pytest
```

## Usage

Run the tool from the command line:

```bash
python smart_debugger.py <traceback_file>
```

Replace `<traceback_file>` with the path to a file containing the Python traceback.

## Testing

Run the tests using pytest:

```bash
pytest test_smart_debugger.py
```

## License

This project is licensed under the MIT License.