# Auto Test Generator

## Description

`auto_test_gen` is a Python tool that leverages OpenAI's API to automatically generate pytest-compatible unit tests for your Python code. By analyzing the input source code, it predicts edge cases, creates relevant test cases, and outputs pytest-compatible test functions. This tool saves developers significant time when writing test suites.

## Features

- Automatically generates pytest-compatible test cases.
- Accepts Python source code as a string or a file path.
- Outputs test cases to a file or returns them as a string.

## Installation

Install the required dependencies:

```bash
pip install openai
```

## Usage

Run the tool from the command line:

```bash
python auto_test_gen.py <source_code_or_path> [--output OUTPUT_FILE] [--api-key OPENAI_API_KEY]
```

### Arguments

- `source_code_or_path`: Path to the Python source code file or the source code as a string.
- `--output`: Path to save the generated test cases. If not provided, the test cases will be printed to the console.
- `--api-key`: OpenAI API key. If not provided, the tool will use the `OPENAI_API_KEY` environment variable.

### Example

Generate test cases for a Python file and save them to `tests.py`:

```bash
python auto_test_gen.py example.py --output tests.py --api-key YOUR_OPENAI_API_KEY
```

## Testing

Run the test suite using `pytest`:

```bash
pytest test_auto_test_gen.py
```

## License

This project is licensed under the MIT License.