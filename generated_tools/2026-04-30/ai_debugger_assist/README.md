# AI Debugger Assist

AI Debugger Assist is a CLI tool that integrates GPT-5.4 or Claude AI to analyze Python stack traces and provide debugging suggestions. It helps developers save time by automating error analysis.

## Features
- Analyze Python stack traces.
- Provide explanations and potential fixes.
- Suggest relevant documentation links.

## Installation

Install the required Python packages:

```bash
pip install openai rich pytest
```

## Usage

Run the tool with a Python stack trace:

```bash
python ai_debugger_assist.py --trace "<your_stack_trace_here>"
```

Example:

```bash
python ai_debugger_assist.py --trace "Traceback (most recent call last):\n  File \"example.py\", line 1, in <module>\n    1 / 0\nZeroDivisionError: division by zero"
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_debugger_assist.py
```

## Notes
- Replace `your_openai_api_key` in the code with your actual OpenAI API key.
- The tool uses mocked API calls for testing purposes.
