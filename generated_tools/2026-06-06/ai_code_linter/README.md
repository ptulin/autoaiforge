# AI Code Linter

## Overview
AI Code Linter is a CLI tool that uses OpenAI's GPT-4 model to analyze your code for stylistic, syntactic, and logical issues. It provides recommendations to improve code readability and maintainability. The tool supports multiple programming languages and integrates seamlessly with popular IDEs.

## Features
- Analyze code for stylistic, syntactic, and logical issues.
- Provide recommendations for improving code quality.
- Support for multiple programming languages (Python, JavaScript, Java, C++).
- Integration with popular IDEs.

## Installation

Install the required Python packages:

```bash
pip install openai rich pytest
```

## Usage

Run the tool from the command line:

```bash
python ai_code_linter.py --path <file_or_directory_path> [--config <config_file_path>]
```

### Arguments
- `--path`: Path to the file or directory to lint (required).
- `--config`: Path to a JSON configuration file (optional).

### Example

```bash
python ai_code_linter.py --path ./my_code.py --config ./config.json
```

## Testing

To run the tests:

```bash
pytest test_ai_code_linter.py
```

## License

This project is licensed under the MIT License.