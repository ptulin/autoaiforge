# Claude Code Assistant

Claude Code Assistant is a command-line tool that integrates with the Claude AI API to provide intelligent code suggestions, fixes, and optimizations directly from the terminal. Developers can input a code snippet, query, or error message, and get immediate feedback, making it ideal for debugging and improving code quality.

## Features

- Get intelligent code suggestions and improvements.
- Request fixes and optimizations for your code.
- Input code via a file or directly as a text argument.
- Save the output to a file or display it in the terminal.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_code_assistant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python claude_code_assistant.py --config <path_to_config> --file <path_to_code_file> [--fix] [--output <path_to_output_file>]
```

### Arguments

- `--config`: Path to the YAML configuration file containing the API URL and API key (required).
- `--file`: Path to the input code file (optional if `--text` is provided).
- `--text`: Code snippet or error message as input (optional if `--file` is provided).
- `--fix`: Request fixes and optimizations for the input code (optional).
- `--output`: Path to save the output suggestions (optional).

### Example

1. Provide code via a file and get suggestions:
   ```bash
   python claude_code_assistant.py --config config.yaml --file example.py
   ```

2. Provide code directly as text and request fixes:
   ```bash
   python claude_code_assistant.py --config config.yaml --text "print('Hello')" --fix
   ```

3. Save the output to a file:
   ```bash
   python claude_code_assistant.py --config config.yaml --file example.py --output suggestions.txt
   ```

## Configuration File

The configuration file should be a YAML file with the following structure:

```yaml
api_url: <your_claude_api_url>
api_key: <your_claude_api_key>
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_claude_code_assistant.py
```

## Requirements

- Python 3.7+
- `requests`
- `pyyaml`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.