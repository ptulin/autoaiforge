# AI Code Snippet Optimizer

## Overview
The AI Code Snippet Optimizer is a Python tool that allows developers to pass small Python code snippets to an AI agent for optimization. The AI improves efficiency, simplifies logic, and suggests alternative approaches for better performance. This tool is ideal for developers seeking to fine-tune critical code paths.

## Features
- Optimize Python code snippets for performance, readability, and maintainability.
- Receive detailed explanations for the changes made by the AI.
- Easy-to-use command-line interface.

## Requirements
- Python 3.7+
- `openai` library
- `rich` library
- `pytest` for testing

## Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install openai rich pytest
   ```
3. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.

## Usage
Run the tool from the command line with the Python code snippet you want to optimize:

```bash
python ai_code_snippet_optimizer.py "def example_function():\n    pass"
```

Example output:

```
[bold green]Optimized Code:[/bold green]
def optimized_function():
    pass

[bold blue]Explanation:[/bold blue]
Simplified the function for better readability.
```

## Testing
To run the tests, use `pytest`:

```bash
pytest test_ai_code_snippet_optimizer.py
```

All tests should pass without requiring network access, as external API calls are mocked.

## License
This project is licensed under the MIT License.