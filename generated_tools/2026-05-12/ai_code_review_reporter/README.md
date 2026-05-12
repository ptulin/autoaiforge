# AI Code Review Reporter

## Description
This tool generates comprehensive reports based on AI code review feedback for a given codebase. It connects to AI reviewers like OpenAI's GPT-4, analyzes their outputs, and formats the results into developer-friendly reports, highlighting issues, suggestions, and actionable insights.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

```bash
python ai_code_review_reporter.py --file <path_to_code_file> --output <path_to_output_report> --format <markdown|html> --api_key <your_openai_api_key>
```

### Arguments

- `--file`: Path to the code file to review (required).
- `--output`: Path to save the generated report (required).
- `--format`: Output format of the report. Options are `markdown` or `html`. Default is `markdown`.
- `--api_key`: Your OpenAI API key (required).

## Example

```bash
python ai_code_review_reporter.py --file example.py --output report.md --format markdown --api_key sk-xxxxxx
```

This will generate a markdown report based on the AI review of `example.py` and save it as `report.md`.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_code_review_reporter.py
```

## Requirements

- Python 3.7+
- `openai`
- `jinja2`

Install dependencies using:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.