# AI Bug Finder

AI Bug Finder is a CLI tool that leverages OpenAI's GPT model to analyze Python codebases, identify potential bugs, and provide detailed explanations and suggestions for fixes. It is designed to help developers improve their code quality efficiently.

## Features

- **AI-Assisted Bug Detection**: Uses AI to scan Python files or directories for potential bugs.
- **Detailed Explanations**: Provides detailed explanations and actionable suggestions for fixing detected issues.
- **File and Directory Support**: Analyze individual Python files or entire directories containing Python scripts.

## Installation

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool using the following command:

```bash
python ai_bug_finder.py --path <path_to_file_or_directory>
```

### Examples

Analyze a single Python file:

```bash
python ai_bug_finder.py --path example.py
```

Analyze an entire directory of Python files:

```bash
python ai_bug_finder.py --path my_codebase/
```

## Requirements

- Python 3.7 or higher
- `openai` library
- `click` library
- `rich` library

## Testing

To run the tests, use:

```bash
pytest test_ai_bug_finder.py
```

## Notes

- Ensure you have an OpenAI API key set in your environment variables as `OPENAI_API_KEY` before running the tool.
- This tool is designed to work with Python files only.

## License

This project is licensed under the MIT License.
