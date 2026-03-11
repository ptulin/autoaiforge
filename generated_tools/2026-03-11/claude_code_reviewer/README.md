# Claude Code Reviewer

Claude Code Reviewer is a command-line tool that leverages Claude AI's enhanced coding capabilities to perform automated code reviews. It allows developers to submit code files or directories, receive feedback, and iterate faster on their projects with the help of Claude.

## Features

- Analyze individual Python files or entire directories containing Python files.
- Send code to the Claude AI API for automated review.
- Save the analysis results to a JSON file.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/claude_code_reviewer.git
   cd claude_code_reviewer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line:

```bash
python claude_code_reviewer.py --path <file_or_directory_path> --api-url <api_endpoint_url> [--output <output_file>]
```

### Arguments

- `--path`: Path to a file or directory to analyze (required).
- `--api-url`: Claude AI API endpoint URL (required).
- `--output`: Output file to save the review report (optional).

### Example

Analyze a single file:

```bash
python claude_code_reviewer.py --path my_script.py --api-url http://fakeapi.com --output report.json
```

Analyze an entire directory:

```bash
python claude_code_reviewer.py --path my_project/ --api-url http://fakeapi.com
```

## Running Tests

To run the tests, use `pytest`:

```bash
pytest test_claude_code_reviewer.py
```

## License

This project is licensed under the MIT License.