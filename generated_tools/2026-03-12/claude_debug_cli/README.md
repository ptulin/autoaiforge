# Claude Debug CLI

Claude Debug CLI is a command-line tool that integrates OpenAI's GPT-4 capabilities to analyze and debug Python scripts. It provides explanations for errors, suggested fixes, and automated corrections.

## Features
- Analyze Python scripts for errors and issues.
- Get detailed explanations and suggested fixes.
- Save the analysis results to an output file.

## Installation

1. Install the required Python packages:

```bash
pip install openai rich
```

2. Save the script to a file, e.g., `claude_debug_cli.py`.

## Usage

Run the script from the command line:

```bash
python claude_debug_cli.py --file <path_to_python_file> --api-key <your_openai_api_key> [--output <output_file>]
```

### Arguments
- `--file`: Path to the Python file to analyze (required).
- `--api-key`: Your OpenAI API key (required).
- `--output`: Optional output file to save the analysis results.

## Example

```bash
python claude_debug_cli.py --file example.py --api-key sk-xxxxxxxx --output analysis.txt
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_claude_debug_cli.py
```

The tests include:
- File not found error handling.
- Empty file error handling.
- OpenAI API error handling (mocked).

## License

This project is licensed under the MIT License.