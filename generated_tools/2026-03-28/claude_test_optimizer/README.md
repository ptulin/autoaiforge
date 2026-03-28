# Claude Test Suite Optimizer

## Overview
The `claude_test_optimizer` is a Python tool that integrates with the Claude AI API to generate optimized test cases for Python code. It uses Claude's advanced AI capabilities to analyze your code and produce robust, corner-case-focused tests to improve code quality.

## Features
- Fetch optimized test cases for your Python code using Claude AI.
- Read Python code from a file.
- Write the generated test cases to an output file.

## Installation
To use this tool, you need to have Python installed along with the following dependencies:

```
pip install requests pytest
```

## Usage
Run the tool from the command line with the following arguments:

```
python claude_test_optimizer.py --code <path_to_python_code> --api-key <your_claude_api_key> [--output <output_file_path>]
```

### Arguments
- `--code`: Path to the Python code file to analyze.
- `--api-key`: Your Claude API key.
- `--output`: (Optional) Path to the output file for the generated test cases. Default is `optimized_tests.py`.

### Example
```
python claude_test_optimizer.py --code my_code.py --api-key my_api_key --output my_tests.py
```

## Testing
To run the tests for this tool, use `pytest`:

```
pytest test_claude_test_optimizer.py
```

The tests include:
- Successful fetching of optimized tests from the Claude API.
- Handling of API errors gracefully.
- Reading code from a file.
- Handling missing files gracefully.
- Writing optimized tests to a file.

## Notes
- Ensure you have a valid Claude API key before using this tool.
- The tool is designed to handle edge cases such as missing files or API errors gracefully.

## License
This project is licensed under the MIT License.