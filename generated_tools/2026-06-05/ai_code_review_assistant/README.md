# AI Code Review Assistant

## Description

The AI Code Review Assistant is a command-line tool that uses OpenAI's GPT model to analyze code files for common errors, antipatterns, and style violations. It provides detailed feedback with suggestions for improvements and highlights potential issues with code readability, efficiency, and maintainability.

## Features

- Analyze individual code files for errors, antipatterns, and style violations.
- Analyze all code files in a specified directory.
- Provides syntax-highlighted code snippets for better readability.
- Displays AI-generated feedback in a user-friendly format.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai_code_review_assistant.git
   cd ai_code_review_assistant
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Analyze a single file

```bash
python ai_code_review_assistant.py --file path/to/your/codefile.py
```

### Analyze a directory

```bash
python ai_code_review_assistant.py --directory path/to/your/directory
```

## Requirements

- Python 3.7+
- `openai`
- `pygments`
- `rich`

## Testing

To run the tests, use:

```bash
pytest test_ai_code_review_assistant.py
```

## Notes

- Ensure you have an OpenAI API key set up in your environment to use this tool.
- The tool uses the `text-davinci-003` engine for code analysis.
