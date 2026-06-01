# Prompt Injection Scanner

## Description
Prompt Injection Scanner is a CLI tool designed to help AI developers identify potential prompt injection vulnerabilities in user-provided inputs. Using heuristic and regex-based detection techniques, this tool scans text inputs or log files to flag suspicious patterns that could compromise the integrity of AI models.

## Features
- Detect common prompt injection patterns using regex.
- Generate actionable reports with flagged inputs and reasons.
- Support for customizable patterns to suit application-specific needs.
- Input via single text or log files.
- Output results to the console or a JSON file.

## Installation
1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/prompt_injection_scanner.git
    cd prompt_injection_scanner
    ```
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
### Scan a log file
```bash
python prompt_injection_scanner.py --input log.txt --output report.json
```

### Scan a single text input
```bash
python prompt_injection_scanner.py --input "Please ignore all previous instructions."
```

### Customize patterns
```bash
python prompt_injection_scanner.py --input log.txt --patterns "(?i)shutdown system" "(?i)execute command"
```

## Example Output
```json
[
    {
        "line": "ignore all previous instructions",
        "reason": "Matched pattern: (?i)ignore\\s+all\\s+previous\\s+instructions"
    }
]
```

## Testing
Run tests using pytest:
```bash
pytest test_prompt_injection_scanner.py
```

## License
This project is licensed under the MIT License.