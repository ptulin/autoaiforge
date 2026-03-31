# AI Code Optimizer

## Overview

AI Code Optimizer is a CLI tool that uses OpenAI's GPT and Anthropic's Claude models to analyze Python scripts and suggest optimizations for performance, readability, and maintainability. This tool is ideal for developers working with AI pipelines or large codebases who want to automate code reviews.

## Features

- Analyze Python scripts for performance, readability, and maintainability improvements.
- Get suggestions from both GPT and Claude models.
- Easy-to-use command-line interface.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool with the following command:

```bash
python ai_code_optimizer.py --file <path_to_python_script> --gpt-key <your_openai_api_key> --claude-key <your_anthropic_api_key>
```

### Example

```bash
python ai_code_optimizer.py --file example.py --gpt-key sk-12345 --claude-key sk-67890
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_optimizer.py
```

## Requirements

- Python 3.7+
- `openai` Python package
- `anthropic` Python package
- `click` Python package
- `pytest` for testing

## License

This project is licensed under the MIT License.