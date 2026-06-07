# AI Code Vulnerability Scanner

## Description
The AI Code Vulnerability Scanner is a command-line tool that scans Python codebases for common security vulnerabilities using a pre-trained AI model fine-tuned on secure coding patterns. It identifies issues such as hardcoded secrets, insecure function usage, and potential injection vulnerabilities, providing specific remediation suggestions.

## Features
- AI-powered detection of security vulnerabilities in Python code.
- Provides precise recommendations for fixing identified issues.
- Scans entire codebases or individual files.
- Outputs a detailed, human-readable report.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_code_vuln_scanner.git
   cd ai_code_vuln_scanner
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To scan a single file:
```bash
python ai_code_vuln_scanner.py --path /path/to/file.py
```

To scan an entire directory:
```bash
python ai_code_vuln_scanner.py --path /path/to/directory
```

## Example Output
```
Scanning file: /path/to/file.py

File: /path/to/file.py

Vulnerabilities
Line    Issue                     Suggestion
----    ------------------------  -----------------------------------
1       Hardcoded secret         Use environment variables instead.
5       Insecure function usage  Use a secure alternative.
```

## Testing
To run the tests:
```bash
pytest test_ai_code_vuln_scanner.py
```

## Limitations
- The tool relies on a pre-trained AI model and may not detect all vulnerabilities.
- False positives or negatives may occur.

## License
This project is licensed under the MIT License.