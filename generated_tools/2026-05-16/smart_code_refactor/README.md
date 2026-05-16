# Smart Code Refactor

## Overview

Smart Code Refactor is a Python tool that uses AI coding assistants to perform intelligent code refactoring. It optimizes code for readability, performance, or specific coding standards, providing suggested changes to improve maintainability and readability.

## Features

- Refactor code for readability, performance, or coding standards.
- View differences between original and refactored code.
- Save refactored code to a file or display it directly in the terminal.

## Installation

1. Clone this repository.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool using the following command:

```bash
python smart_code_refactor.py --file <path_to_code_file> --goal <refactoring_goal> [--output <output_file>]
```

### Arguments

- `--file`: Path to the code file to refactor (required).
- `--goal`: Refactoring goal. Choose from `readability`, `performance`, or `standards` (required).
- `--output`: Path to save the refactored code. If not provided, the refactored code will be displayed in the terminal.

### Example

```bash
python smart_code_refactor.py --file example.py --goal readability --output refactored_example.py
```

## Testing

To run the tests, use the following command:

```bash
pytest test_smart_code_refactor.py
```

## Requirements

- Python 3.7+
- `openai`
- `python-dotenv`
- `diff-match-patch`
- `pytest`

## Environment Variables

Set up the `OPENAI_API_KEY` environment variable in a `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## License

This project is licensed under the MIT License.