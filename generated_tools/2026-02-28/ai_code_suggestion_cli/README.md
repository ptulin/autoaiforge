# AI Code Suggestion CLI

## Overview
The AI Code Suggestion CLI is a Python-based command-line tool that integrates with AI coding assistants to provide real-time code suggestions. Developers can use this tool to get quick code snippets based on a function description or partial code snippet without switching to an IDE.

## Features
- Fetch code suggestions from an AI API based on a description and programming language.
- Save the suggested code snippet to a file or display it in the terminal.

## Requirements
- Python 3.7+
- `requests` library
- `pytest` library (for testing)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai_code_suggestion_cli
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:
   ```bash
   export OPENAI_API_KEY=your_api_key_here
   ```

2. Run the CLI tool:
   ```bash
   python ai_code_suggestion_cli.py --description "function to add two numbers" --language python
   ```

3. Optionally, save the output to a file:
   ```bash
   python ai_code_suggestion_cli.py --description "function to add two numbers" --language python --output suggestion.py
   ```

## Testing
To run the tests, use:
```bash
pytest test_ai_code_suggestion_cli.py
```

The tests include:
- Successful API response handling.
- Handling missing API key.
- Handling API errors.

## License
This project is licensed under the MIT License.