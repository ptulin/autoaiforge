# Code Review AI

## Overview

Code Review AI is a command-line tool that uses OpenAI's API to analyze Python scripts or projects. It identifies potential bugs, provides optimization suggestions, and offers coding best practices. This tool is useful for developers who want instant feedback on their code to improve quality and performance.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd code_review_ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

### Analyze a single file
```bash
python code_review_ai.py --file <path_to_python_file>
```

### Analyze all Python files in a directory
```bash
python code_review_ai.py --directory <path_to_directory>
```

### Save the analysis report to a file
```bash
python code_review_ai.py --file <path_to_python_file> --output <output_file>
```

### Example

Analyze a single file:
```bash
python code_review_ai.py --file example.py
```

Analyze all Python files in a directory and save the report:
```bash
python code_review_ai.py --directory ./my_project --output report.txt
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_code_review_ai.py
```

## Requirements

- Python 3.7+
- `openai` library
- `click` library

Install dependencies using:
```bash
pip install -r requirements.txt
```

## Notes

- You need an OpenAI API key to use this tool. Set the `OPENAI_API_KEY` environment variable to your API key before running the tool.
- The tool is designed to handle errors gracefully, such as missing files or directories, and invalid input.
