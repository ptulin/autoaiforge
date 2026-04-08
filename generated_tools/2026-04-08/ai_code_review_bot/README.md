# AI Code Review Bot

This tool integrates AI-based code review into a developer's workflow by analyzing code for potential issues, providing suggestions for improvement, and generating alternative, optimized solutions. It can be used as a CLI tool or integrated into CI/CD pipelines for automated code quality checks.

## Features
- Analyze Python code for readability, performance, and other issues.
- Generate detailed suggestions for improvement using OpenAI's GPT-4.
- Process individual files or entire directories.
- Generate rich reports in the terminal or save them to a file.

## Installation

Install the required dependencies:

```bash
pip install openai rich
```

## Usage

### CLI

```bash
python ai_code_review_bot.py <path> <review_type> [--output <output_file>]
```

- `<path>`: Path to the file or directory to review.
- `<review_type>`: Type of review to perform (e.g., readability, performance).
- `--output <output_file>`: (Optional) File path to save the report.

### Example

```bash
python ai_code_review_bot.py my_script.py readability --output report.txt
```

### Environment Variables

Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Testing

Run tests using `pytest`:

```bash
pytest test_ai_code_review_bot.py
```

## License

MIT License
