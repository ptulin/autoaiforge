# AI Code Refactor

## Description

AI Code Refactor is a Python tool that allows developers to refactor their Python code with the help of the OpenAI API. It can rename variables, functions, and classes to follow specific naming conventions, restructure code for better readability, or optimize performance. The tool also formats the refactored code using the Black code formatter.

## Features

- Rename variables, functions, and classes to follow specific naming conventions.
- Restructure code for better readability.
- Optimize code for improved performance.
- Automatically formats the refactored code using Black.

## Installation

Install the required dependencies using pip:

```bash
pip install openai black click pytest
```

## Usage

Run the tool from the command line:

```bash
python ai_code_refactor.py --file <input_file_path> --output <output_file_path> [--rename-vars] [--restructure-code] [--optimize-performance]
```

### Options

- `--file`: Path to the Python file to refactor (required).
- `--output`: Path to save the refactored Python file (required).
- `--rename-vars`: Enable renaming of variables and functions (optional).
- `--restructure-code`: Enable restructuring of code for better readability (optional).
- `--optimize-performance`: Enable performance optimization (optional).

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_refactor.py
```

The tests include:

1. Verifying that the tool raises a `FileNotFoundError` when the input file does not exist.
2. Mocking the OpenAI API and Black formatter to test successful refactoring.
3. Testing error handling when the OpenAI API returns an error.

## Notes

- Ensure you have a valid OpenAI API key set in your environment to use this tool.
- The tool requires internet access to communicate with the OpenAI API.
