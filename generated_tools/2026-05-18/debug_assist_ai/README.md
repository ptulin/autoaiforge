# Debug Assist AI

Debug Assist AI is a Python CLI tool that analyzes error messages or stack traces and generates AI-powered suggestions for resolving issues. It integrates with OpenAI's API to provide explanations, potential solutions, and relevant code fixes.

## Features
- Analyze Python error messages or stack traces.
- Generate AI-powered debugging suggestions.
- Supports input via command-line arguments or piped input.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd debug_assist_ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Usage

You can use the tool by providing an error message or stack trace as an argument or by piping input to it.

#### Example 1: Using `--error_message` argument
```bash
python debug_assist_ai.py --error_message "IndexError: list index out of range"
```

#### Example 2: Piping input
```bash
echo "IndexError: list index out of range" | python debug_assist_ai.py
```

### Output
The tool will output AI-generated suggestions for debugging and fixing the provided error message or stack trace.

## Running Tests

To run the tests, install `pytest`:
```bash
pip install pytest
```

Then run:
```bash
pytest test_debug_assist_ai.py
```

## Requirements
- Python 3.7+
- `openai` package

## Notes
- You need an OpenAI API key to use this tool. Set the `OPENAI_API_KEY` environment variable with your API key before running the tool.

## License
This project is licensed under the MIT License.