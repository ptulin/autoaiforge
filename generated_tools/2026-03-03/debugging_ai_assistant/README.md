# Debugging AI Assistant

## Overview
The Debugging AI Assistant is a Python tool that integrates with your IDE to assist in debugging Python code. It analyzes stack traces and runtime errors using OpenAI's API and provides actionable suggestions, potential root causes, and code edits to simplify the debugging process.

## Features
- Analyze Python scripts and error messages.
- Provide AI-suggested fixes and explanations.
- Highlight suggestions in terminal using Pygments.

## Installation

Install the required dependencies:

```bash
pip install openai pygments
```

## Usage

Run the tool from the command line:

```bash
python debugging_ai_assistant.py --file <path_to_python_script> --error <error_message>
```

Example:

```bash
python debugging_ai_assistant.py --file example.py --error "IndexError: list index out of range"
```

## Testing

Run the tests using pytest:

```bash
pytest test_debugging_ai_assistant.py
```

## License

This project is licensed under the MIT License.