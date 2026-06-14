# AI Debug Assistant

AI Debug Assistant is a CLI tool that uses OpenAI's GPT model to analyze Python error messages and provide debugging suggestions, including explanations, potential causes, and code snippets to help developers resolve issues efficiently.

## Features
- Analyze Python error messages.
- Get detailed debugging suggestions.
- Supports input via CLI arguments or log files.

## Installation

Install the required Python packages:

```bash
pip install openai rich pytest
```

## Usage

### CLI

Provide an error message directly:

```bash
python ai_debug_assistant.py --error "NameError: name 'x' is not defined"
```

Or provide a log file containing the error message:

```bash
python ai_debug_assistant.py --logfile path/to/logfile.txt
```

### Environment Variables

Set the `OPENAI_API_KEY` environment variable to authenticate with the OpenAI API:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## Testing

Run tests using pytest:

```bash
pytest test_ai_debug_assistant.py
```

## License

This project is licensed under the MIT License.