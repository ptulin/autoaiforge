# Debug Sentinel

Debug Sentinel is a Python tool that integrates with AI coding assistants to analyze runtime errors and suggest fixes in real-time. By analyzing stack traces, it provides concise explanations and suggests code modifications to resolve issues efficiently.

## Features

- Analyze Python stack traces.
- Get suggestions for fixing runtime errors.
- Output results in either plain text or JSON format.

## Installation

1. Install the required Python packages:

```bash
pip install openai pytest
```

2. Save the `debug_sentinel.py` file to your desired location.

## Usage

Run the tool from the command line:

```bash
python debug_sentinel.py <path_to_stack_trace_file> --api-key <your_openai_api_key> [--output-format text|json]
```

### Arguments

- `input`: Path to the file containing the Python stack trace.
- `--api-key`: Your OpenAI API key (required).
- `--output-format`: Output format for suggestions. Options are `text` (default) or `json`.

### Example

```bash
python debug_sentinel.py stack_trace.txt --api-key sk-abc123 --output-format json
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_debug_sentinel.py
```

The tests include:

- Mocked OpenAI API responses to ensure no network calls are made.
- Validation of text and JSON output formats.
- Handling of empty stack traces.

## License

This project is licensed under the MIT License.