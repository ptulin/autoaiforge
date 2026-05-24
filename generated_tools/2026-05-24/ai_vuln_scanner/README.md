# AI-Powered Vulnerability Scanner

## Description
The AI-Powered Vulnerability Scanner (`ai_vuln_scanner`) is a command-line tool that leverages AI models to scan source code files or entire repositories for potential vulnerabilities. It provides detailed reports and actionable remediation suggestions, making it an ideal tool for developers looking to automate security checks in their development workflows.

## Features
- **Scan Individual Files or Entire Codebases**: Analyze a single file or recursively scan all files in a directory.
- **AI-Powered Analysis**: Leverages advanced AI models to detect vulnerabilities and provide recommendations.
- **Human-Readable Reports**: View results directly in the terminal or export them to a JSON file for further analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_vuln_scanner.git
   cd ai_vuln_scanner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python ai_vuln_scanner.py --path <file_or_directory_path> [--output <output_file>]
```

### Examples
- Scan a single file:
  ```bash
  python ai_vuln_scanner.py --path ./example.py
  ```

- Scan a directory and save the report to a JSON file:
  ```bash
  python ai_vuln_scanner.py --path ./my_project --output report.json
  ```

## Requirements
- Python 3.7+
- `openai==0.27.8`
- `rich==13.5.2`

## Testing
Run the tests using `pytest`:
```bash
pytest test_ai_vuln_scanner.py
```

The tests include mocking for external API calls and cover the following scenarios:
1. Scanning a single file.
2. Scanning a directory with multiple files.
3. Generating a JSON report.

## License
This project is licensed under the MIT License.
