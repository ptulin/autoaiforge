# AI Code Suggester

AI Code Suggester is a Python tool that integrates with Claude AI to provide real-time code suggestions for Python files. It analyzes partially written functions and generates inline suggestions for completing them, making it useful for quick prototyping or learning new APIs.

## Features
- Analyze Python files and get code suggestions.
- Add suggestions inline as comments or display them in the terminal.

## Installation

Install the required dependencies:

```bash
pip install openai rich
```

## Usage

Run the tool with the following command:

```bash
python ai_code_suggester.py --file <path_to_file> --api-key <your_openai_api_key>
```

### Options
- `--file`: Path to the Python file to analyze (required).
- `--api-key`: OpenAI API key (required).
- `--model`: Claude AI model to use (default: `claude-v1`).
- `--max-tokens`: Maximum tokens for the AI response (default: 150).
- `--inline`: Add suggestions inline as comments in the file.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_suggester.py
```

## License

This project is licensed under the MIT License.