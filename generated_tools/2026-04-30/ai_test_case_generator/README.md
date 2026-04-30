# AI Test Case Generator

## Overview
The AI Test Case Generator is a Python CLI tool that uses OpenAI's GPT models to automatically generate pytest test cases for a given Python module or function. This tool helps developers save time by automating the creation of test cases, promoting better code coverage and reducing repetitive tasks.

## Features
- Generate pytest test cases for an entire Python file or a specific function.
- Save the generated test cases to a specified output file.
- Supports parameterized tests and includes comments for better understanding.

## Requirements
- Python 3.7+
- `openai` package
- `click` package
- `pytest` package (for testing the tool)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai_test_case_generator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To use the AI Test Case Generator, run the following command:

```bash
python ai_test_case_generator.py --file <path_to_python_file> --output <path_to_output_file> --api-key <your_openai_api_key>
```

### Options
- `--file`: Path to the Python file for which you want to generate test cases (required).
- `--function`: (Optional) Specify a function name to generate test cases only for that function.
- `--output`: Path to save the generated test cases (required).
- `--api-key`: Your OpenAI API key (required). You can also set this as an environment variable `OPENAI_API_KEY`.

### Example
Generate test cases for a Python file:
```bash
python ai_test_case_generator.py --file example.py --output test_example.py --api-key YOUR_API_KEY
```

Generate test cases for a specific function in a Python file:
```bash
python ai_test_case_generator.py --file example.py --function my_function --output test_example.py --api-key YOUR_API_KEY
```

## Testing
To run the tests for this tool, use pytest:

```bash
pytest test_ai_test_case_generator.py
```

## License
This project is licensed under the MIT License.
