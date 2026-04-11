# AI Refactor Assistant

AI Refactor Assistant is a Python library that provides an interface for AI-assisted code refactoring. Developers can pass their scripts or functions, and the tool suggests improvements in readability, performance, or adherence to best practices. This is especially useful for optimizing legacy codebases or improving development standards.

## Features

- **AI-driven code quality analysis**: Leverages OpenAI's GPT-4 to provide intelligent suggestions for improving your code.
- **Performance optimizations**: Identifies potential performance bottlenecks and suggests improvements.
- **Automatic formatting**: Uses the Black code formatter to ensure consistent and clean code style.

## Installation

Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

You can use the AI Refactor Assistant as a library or from the command line.

### As a Library

```python
from ai_refactor_assistant import refactor_code

# Example usage
input_code = """
def add(a, b):
    return a + b
"""

refactored_code = refactor_code(input_code, openai_api_key="your_openai_api_key")
print(refactored_code)
```

### From the Command Line

```bash
python ai_refactor_assistant.py "path/to/your_script.py" --output_file "refactored_script.py" --openai_api_key "your_openai_api_key"
```

If you don't provide an output file, the refactored code will be printed to the console.

## Requirements

- Python 3.7+
- `openai==0.27.8`
- `black==23.9.1`
- `pytest==7.4.2`

## Testing

Run the tests using pytest:

```bash
pytest test_ai_refactor_assistant.py
```

## Example

Input Code:

```python
def add(a, b):
    return a + b
```

Refactored Code:

```python
def add(a, b):
    return a + b
```

## License

This project is licensed under the MIT License.
