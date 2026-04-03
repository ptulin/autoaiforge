# Auto Snippet Generator

## Overview
The Auto Snippet Generator is a Python tool that leverages the OpenAI API to generate reusable Python code snippets for common programming tasks. Developers can provide a brief description of the problem or functionality they need, and the tool will generate optimized Python code snippets tailored to their needs.

## Features
- Generate Python code snippets based on natural language prompts.
- Optionally specify a framework or library to use in the generated code.
- Save the generated code snippet to a file.

## Installation
To use this tool, you need to install the required Python packages:

```bash
pip install openai click pytest
```

## Usage
1. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

2. Run the tool using the command line:

```bash
python auto_snippet_generator.py --prompt "create a function to read a file" --framework "pandas" --output "snippet.py"
```

### Options
- `--prompt`: Description of the task for which to generate a code snippet (required).
- `--framework`: Optional framework or library to use in the code snippet.
- `--output`: Optional file path to save the generated code snippet.

## Testing
To run the tests:

```bash
pytest test_auto_snippet_generator.py
```

The tests include:
- Successful generation of code snippets.
- Handling of missing API keys.
- Handling of OpenAI API errors.

## License
This project is licensed under the MIT License.