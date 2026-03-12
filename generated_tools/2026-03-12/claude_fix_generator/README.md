# Claude Fix Generator

## Overview

Claude Fix Generator is an automation tool that uses Claude AI to scan a project directory for Python files, identify common coding issues, and auto-generate suggested fixes. It outputs a summary report and optionally applies fixes to a copy of the codebase.

## Features

- Scans a project directory for Python files.
- Analyzes Python files for coding issues using Claude AI.
- Generates a JSON report with suggested fixes.
- Optionally applies fixes to a copy of the project directory.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/claude-fix-generator.git
   cd claude-fix-generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python claude_fix_generator.py --project-dir <path_to_project> --api-key <your_api_key> [--apply-fixes] [--output-dir <output_directory>] [--report-file <report_file>]
```

### Arguments

- `--project-dir`: Path to the project directory containing Python files (required).
- `--api-key`: OpenAI API key for Claude AI (required).
- `--apply-fixes`: Apply fixes to a copy of the project (optional).
- `--output-dir`: Directory to save the fixed project (default: `./fixed_project`).
- `--report-file`: Path to save the JSON report (default: `report.json`).

## Testing

Run the tests using pytest:

```bash
pytest test_claude_fix_generator.py
```

## License

This project is licensed under the MIT License.