# AI Zero-Day Scanner

AI Zero-Day Scanner is a CLI tool that leverages pre-trained AI models to perform static code analysis and detect potential zero-day vulnerabilities. This tool is useful for developers who want to identify security flaws in their codebase before deployment.

## Features
- Analyze Python files for potential vulnerabilities.
- Generate detailed vulnerability reports.
- Easy-to-use CLI interface.

## Installation

Install the required dependencies:

```bash
pip install transformers rich pygments
```

## Usage

Run the tool using the following command:

```bash
python ai_zero_day_scanner.py --path <path_to_file_or_directory> [--output <output_report_path>]
```

- `--path`: Path to the file or directory to scan.
- `--output`: (Optional) Path to save the output report.

## Example

Analyze a single file:

```bash
python ai_zero_day_scanner.py --path example.py
```

Analyze all Python files in a directory:

```bash
python ai_zero_day_scanner.py --path ./my_project
```

Save the report to a file:

```bash
python ai_zero_day_scanner.py --path example.py --output report.txt
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_zero_day_scanner.py
```

## License

This project is licensed under the MIT License.