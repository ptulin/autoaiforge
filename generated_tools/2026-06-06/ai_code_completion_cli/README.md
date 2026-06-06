# AI Code Completion CLI

## Description

The AI Code Completion CLI is a lightweight command-line tool that leverages OpenAI's API to provide AI-driven code completions for partially written scripts. Developers can pass incomplete code files or snippets, and the tool generates plausible completions based on the context.

## Features

- Accepts input from a file containing incomplete code or a code snippet.
- Uses OpenAI's `text-davinci-003` model to generate code completions.
- Allows customization of the maximum number of tokens for the completion.

## Requirements

- Python 3.7+
- `openai` Python package
- `pytest` for testing

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the tool, run the following command:

```bash
python ai_code_completion_cli.py --input <path_to_input_file> --api-key <your_openai_api_key> [--max-tokens <number_of_tokens>]
```

### Arguments

- `--input`: Path to the input file containing incomplete code or a code snippet (required).
- `--api-key`: Your OpenAI API key (required).
- `--max-tokens`: Maximum number of tokens to generate for the completion (default: 150).

### Example

```bash
python ai_code_completion_cli.py --input example.py --api-key sk-xxxxxxxx --max-tokens 100
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_ai_code_completion_cli.py
```

The tests include mocking for external API calls and file operations, so no actual network access or file creation is required.

## License

This project is licensed under the MIT License.