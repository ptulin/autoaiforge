# AI Debug Assist

AI Debug Assist is a CLI tool that integrates with AI coding agents like OpenAI's GPT models to analyze error logs, tracebacks, or bugs in your code, and provide intelligent debugging suggestions directly in the terminal. The tool automates troubleshooting by combining AI reasoning with contextual awareness of your project.

## Features
- Analyze error logs and tracebacks.
- Provide step-by-step debugging suggestions.
- Contextual awareness of your codebase.

## Installation

Install the required Python packages:

```bash
pip install openai rich
```

## Usage

Run the tool using the following command:

```bash
python ai_debug_assist.py --api-key YOUR_API_KEY --error-log PATH_TO_ERROR_LOG --code-path PATH_TO_CODE_DIRECTORY
```

### Arguments
- `--api-key`: Your OpenAI API key.
- `--error-log`: Path to the error log file.
- `--code-path`: Path to the code directory for context.

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_ai_debug_assist.py
```

## License

This project is licensed under the MIT License.