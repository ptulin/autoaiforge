# AI Debugger Assistant

## Description
The AI Debugger Assistant is a command-line tool that helps developers debug Python scripts by analyzing error tracebacks and providing AI-powered suggestions for fixes. The tool uses OpenAI's GPT-4 model to analyze the script and error logs, offering detailed explanations and recommendations.

## Features
- Analyze Python scripts and error tracebacks.
- Get AI-generated suggestions for fixing errors.
- Detailed explanations of issues in the code.

## Installation
1. Clone the repository or download the script.
2. Install the required dependencies:
   ```bash
   pip install openai rich
   ```

## Usage
Run the tool from the command line with the following arguments:

```bash
python ai_debugger_assistant.py --file <path_to_python_script> [--error-log <error_log>]
```

### Arguments
- `--file`: Path to the Python script file to analyze. (Required)
- `--error-log`: Optional error log or traceback to provide additional context.

### Example
```bash
python ai_debugger_assistant.py --file example.py --error-log "Traceback (most recent call last): ..."
```

## Testing
To run the tests, install `pytest` and execute the following command:

```bash
pytest test_ai_debugger_assistant.py
```

The tests include:
- Handling of non-existent files.
- Successful AI response.
- Handling of AI-related errors.

## Notes
- Ensure you have an OpenAI API key set up in your environment to use this tool.
- This tool requires an active internet connection to communicate with the OpenAI API.
