# Claude Code Review

`claude_code_review` is a CLI tool that performs automated code reviews by leveraging Claude AI's coding capabilities. It provides detailed feedback on potential bugs, style issues, and optimizations, helping developers improve their code quality.

## Features
- Analyze Python code for potential bugs, style issues, and optimizations.
- Display feedback in a user-friendly, styled CLI report.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/claude_code_review.git
   cd claude_code_review
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line:

```bash
python claude_code_review.py --file <path_to_python_file> --api-key <your_claude_api_key>
```

- `--file`: Path to the Python file you want to review.
- `--api-key`: Your Claude API key.

## Example

```bash
python claude_code_review.py --file example.py --api-key your_api_key_here
```

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_claude_code_review.py
```

## Requirements

- Python 3.7+
- `requests`
- `rich`

## License

This project is licensed under the MIT License.