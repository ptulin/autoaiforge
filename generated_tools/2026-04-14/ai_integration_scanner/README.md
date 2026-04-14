# AI Integration Security Scanner

## Description
The AI Integration Security Scanner is a command-line tool designed to help developers identify and address security vulnerabilities in Python codebases that integrate with AI services. It scans for common issues such as hardcoded API keys, unencrypted HTTP requests, and unsafe usage of functions like `eval` or `exec`.

## Features
- Detects hardcoded API keys in Python files.
- Identifies unencrypted HTTP requests to AI endpoints.
- Flags unsafe usage of `eval` and `exec` functions.
- Provides line numbers and actionable recommendations for fixing issues.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_integration_scanner.git
   cd ai_integration_scanner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the scanner on a specific file:
```bash
python ai_integration_scanner.py --path ./example.py
```

Run the scanner on a directory:
```bash
python ai_integration_scanner.py --path ./my_project
```

## Example Output
```
File: ./example.py, Line: 3
Issue: Hardcoded API key detected.
Recommendation: Remove hardcoded API keys and use environment variables instead.

File: ./example.py, Line: 5
Issue: Unencrypted HTTP request detected.
Recommendation: Use HTTPS instead of HTTP for secure communication.
```

## License
MIT License