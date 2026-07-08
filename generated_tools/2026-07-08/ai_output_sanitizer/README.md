# AI Output Sanitizer

## Overview
The AI Output Sanitizer is a Python tool designed to scan AI-generated text outputs for sensitive data patterns, such as API keys, secrets, or private URLs. It can flag or mask sensitive data to help developers ensure that AI outputs do not inadvertently expose private information.

## Features
- Scans text for sensitive data patterns using customizable rules.
- Flags or masks sensitive data based on user preference.
- Supports JSON-based rule definitions for flexibility.

## Installation
1. Clone the repository or download the script.
2. Install the required Python package:
   ```bash
   pip install colorama
   ```

## Usage
Run the script from the command line:
```bash
python ai_output_sanitizer.py --input <input_file> --rules <rules_file> [--mask]
```

### Arguments
- `--input`: Path to the input text file to be scanned.
- `--rules`: Path to the JSON file containing detection rules.
- `--mask`: Optional flag to mask sensitive data instead of just flagging it.

### Example
```bash
python ai_output_sanitizer.py --input sample.txt --rules rules.json --mask
```

## Rules File Format
The rules file should be a JSON file containing an array of rule objects. Each rule object must have a `pattern` (regex) and an optional `description`.

### Example Rules File
```json
[
  {"pattern": "\\d{5}-[A-Z]{5}", "description": "API Key"},
  {"pattern": "http://[a-zA-Z0-9.-]+", "description": "Private URL"}
]
```

## Testing
To run the tests, install `pytest` and execute:
```bash
pytest test_ai_output_sanitizer.py
```

## License
This project is licensed under the MIT License.