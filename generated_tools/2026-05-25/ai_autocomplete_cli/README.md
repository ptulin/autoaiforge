# AI Autocomplete CLI

## Description
AI Autocomplete CLI is a command-line tool that uses AI models such as OpenAI Codex to provide intelligent code autocompletion suggestions. Developers can pipe code snippets into the tool, and it will return multiple completion options based on the input context. This tool is ideal for rapid prototyping or debugging.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/ai_autocomplete_cli.git
   cd ai_autocomplete_cli
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Example Usage
```bash
# Pipe a code snippet into the tool
echo 'def factorial(n):' | python ai_autocomplete_cli.py --model text-davinci-003 --output-format json

# Output in plain text
echo 'def factorial(n):' | python ai_autocomplete_cli.py --model text-davinci-003 --output-format text
```

### Options
- `--model`: Specify the AI model to use for code completion (default: `text-davinci-003`).
- `--output-format`: Specify the output format (`json` or `text`). Default is `json`.

## Features
- **AI-powered code autocompletion**: Leverages OpenAI models for intelligent code suggestions.
- **Multiple completion options**: Provides three different code completion suggestions.
- **Flexible input and output**: Accepts input via stdin and supports JSON or plain text output formats.

## Testing
Run the tests using pytest:
```bash
pytest test_ai_autocomplete_cli.py
```

## License
This project is licensed under the MIT License.
