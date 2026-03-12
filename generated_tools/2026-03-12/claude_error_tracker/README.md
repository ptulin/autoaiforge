# Claude Error Tracker

Claude Error Tracker is a Python library that integrates with Claude AI to monitor and track runtime errors in Python applications. It captures errors, sends them to Claude for analysis, and logs detailed correction suggestions for developers.

## Features

- Automatically captures uncaught exceptions in Python applications.
- Sends error details to Claude AI for analysis.
- Logs detailed suggestions from Claude AI to help developers debug their code.

## Installation

Install the required dependencies using pip:

```bash
pip install openai pytest
```

## Usage

Run the script with your Claude API key:

```bash
python claude_error_tracker.py --api_key YOUR_API_KEY
```

This will start the error tracker and simulate an error for demonstration purposes.

## Testing

To run the tests, use pytest:

```bash
pytest test_claude_error_tracker.py
```

The tests include mocking for external API calls, so no network access is required.

## License

This project is licensed under the MIT License.