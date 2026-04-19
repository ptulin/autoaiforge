# UX Audit Generator

## Description
The UX Audit Generator is an automation tool that uses the Claude Design API to perform automated audits of UI/UX prototypes. It evaluates designs for usability, accessibility, and aesthetic consistency based on well-known UX principles and generates a detailed audit report in either HTML or Markdown format.

## Features
- Automated UX audit of prototypes using Claude Design API
- Checks for accessibility compliance and usability best practices
- Generates detailed, human-readable audit reports in HTML or Markdown

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ux-audit-generator.git
   cd ux-audit-generator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:
```bash
python ux_audit_generator.py --input prototype.json --output report.md --api-url https://api.claude.design/audit --api-key YOUR_API_KEY
```

### Arguments
- `--input`: Path to the prototype JSON file (required)
- `--output`: Path to save the generated report (required)
- `--api-url`: URL of the Claude Design API (required)
- `--api-key`: API key for authentication (required)
- `--description`: Optional text description of the prototype
- `--format`: Output format, either `html` or `md` (default: `md`)

### Example
```bash
python ux_audit_generator.py \
  --input example_prototype.json \
  --output audit_report.md \
  --api-url https://api.claude.design/audit \
  --api-key YOUR_API_KEY \
  --description "This is a prototype for a mobile app."
```

## Testing
To run the tests, use:
```bash
pytest test_ux_audit_generator.py
```

## License
This project is licensed under the MIT License.
