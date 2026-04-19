# AI Code Linter

AI Code Linter is a Python library and CLI tool that uses OpenAI's GPT models and Pylint to analyze Python code for potential issues, style violations, and bugs. It can integrate into CI/CD pipelines or be used locally to ensure high-quality code standards.

## Features

- Analyze Python code for issues using Pylint.
- Use OpenAI's GPT models to provide suggestions and improvements for your code.
- Process individual files or entire directories.
- Optional auto-fix functionality (future feature).

## Installation

Install the required dependencies:

```bash
pip install openai pylint
```

## Usage

Run the tool from the command line:

```bash
python ai_code_linter.py --path <path_to_file_or_directory> --api-key <your_openai_api_key>
```

### Options

- `--path`: Path to the Python file or directory to lint.
- `--fix`: Automatically fix issues where possible (currently a placeholder).
- `--api-key`: Your OpenAI API key for AI analysis.

## Example

```bash
python ai_code_linter.py --path my_script.py --api-key sk-xxxxxxxxxxxxxxxxxxxx
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_linter.py
```

## License

This project is licensed under the MIT License.