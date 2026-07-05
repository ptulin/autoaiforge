# Code Debug AI Assistant

## Description
Code Debug AI Assistant is a command-line tool designed to help developers debug Python code. By providing error messages, stack traces, or problematic code as input, the tool uses OpenAI's GPT model to suggest debugging steps, potential fixes, and educational explanations for errors. This tool empowers developers to learn from the debugging process while resolving issues efficiently.

## Features
- Analyze Python error messages and stack traces.
- Suggest debugging steps and fixes.
- Provide educational explanations for errors.
- Output results to the console or save them to a YAML file.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd code_debug_ai_assistant
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Input via File
Provide an input file containing the error message, stack trace, or problematic code:
```bash
python code_debug_ai_assistant.py --input error_log.txt --output suggestions.yaml
```

### Input via Stdin
You can also provide input directly via stdin:
```bash
python code_debug_ai_assistant.py --output suggestions.yaml
```
Then type your input and press `Ctrl+D` to submit.

### Output
- If `--output` is specified, the suggestions will be saved to the specified YAML file.
- If `--output` is not specified, the suggestions will be printed to the console.

## Example
Input (via file or stdin):
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

Output (console or YAML file):
```
suggestions: Here are some debugging suggestions.
```

## Development

### Running Tests
To run tests, install `pytest` and execute:
```bash
pytest test_code_debug_ai_assistant.py
```

### Mocking OpenAI API
The tests use `unittest.mock` to mock OpenAI API calls, ensuring no real API calls are made during testing.

## License
This project is licensed under the MIT License.