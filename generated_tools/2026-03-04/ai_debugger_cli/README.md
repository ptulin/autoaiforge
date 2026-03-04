# AI Debugger CLI

AI Debugger CLI is a command-line tool designed to help developers analyze Python stack traces and error messages using Claude AI. It provides detailed explanations of errors and suggests fixes directly in the terminal, saving time and reducing context switching.

## Features

- Parses Python stack traces and runtime errors.
- Sends error context to Claude AI for debugging insights.
- Provides detailed explanations and fix recommendations.
- Supports input via file or stdin.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai_debugger_cli.git
   cd ai_debugger_cli
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Analyze Error Logs from a File

```bash
python ai_debugger_cli.py --file error_log.txt
```

### Analyze Error Logs from Stdin

```bash
cat error_log.txt | python ai_debugger_cli.py
```

### Example Input

```plaintext
Traceback (most recent call last):
  File "example.py", line 1, in <module>
    1/0
ZeroDivisionError: division by zero
```

### Example Output

```plaintext
╭──────────────────────────────────────────────────────╮
│                  AI Debugger Response               │
├──────────────────────────────────────────────────────┤
│ The error is a ZeroDivisionError, which occurs when │
│ you attempt to divide a number by zero. To fix this │
│ issue, ensure that the denominator is not zero.     │
╰──────────────────────────────────────────────────────╯
```

## Development

### Running Tests

Install `pytest`:
```bash
pip install pytest
```

Run the tests:
```bash
pytest
```

## License

MIT License