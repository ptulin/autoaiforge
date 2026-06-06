# AI Debug Prompt Generator

## Description
The AI Debug Prompt Generator is a Python tool designed to help developers efficiently query AI coding assistants for solutions to errors in their code. By parsing error logs and stack traces, the tool generates concise and actionable debugging prompts tailored to the specific issue.

## Features
- Parses error logs and stack traces into actionable data.
- Generates AI-compatible debugging prompts.
- Supports multiple programming languages and frameworks.

## Installation

Install the required dependencies:

```bash
pip install openai==0.27.0
```

## Usage

Run the tool with an error log file as input:

```bash
python ai_debug_prompt_generator.py --error-log error_log.txt
```

Example output:

```
Generated Debugging Prompt:
I encountered an error in my code. The error type is 'ValueError' with the message: 'Invalid value'. Here is the stack trace: 
Traceback (most recent call last):
  File "example.py", line 10, in <module>
    raise ValueError('Invalid value')
ValueError: Invalid value
Can you help me understand what might be causing this issue and how to resolve it?
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_debug_prompt_generator.py
```

## License
MIT License
