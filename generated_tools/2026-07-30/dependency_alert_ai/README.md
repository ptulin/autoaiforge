# Dependency Alert AI

Dependency Alert AI is a Python-based command-line tool designed to analyze your project's dependencies for known vulnerabilities. It cross-references dependency versions with public vulnerability databases (e.g., NVD) and provides actionable recommendations for upgrading or patching.

## Features
- AI-enhanced dependency vulnerability detection
- Integration with public vulnerability databases (e.g., NVD)
- Provides actionable upgrade/patch suggestions
- Supports plain-text and JSON output formats

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dependency_alert_ai.git
   cd dependency_alert_ai
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with a `requirements.txt` file as input:

```bash
python dependency_alert_ai.py --requirements requirements.txt
```

You can also specify the output format as JSON:

```bash
python dependency_alert_ai.py --requirements requirements.txt --output json
```

## Example

Given a `requirements.txt` file:

```
example==1.0.0
anotherpackage==2.3.4
```

The tool will output:

```
Package: example
Version: 1.0.0
Vulnerabilities:
  - CVE-2023-1234: Test vulnerability.

Package: anotherpackage
Version: 2.3.4
Vulnerabilities:
  - CVE-2023-5678: Another test vulnerability.
```

Or in JSON format:

```json
{
    "example": {
        "version": "1.0.0",
        "vulnerabilities": [
            {
                "CVE_data_meta": {"ID": "CVE-2023-1234"},
                "description": {"description_data": [{"value": "Test vulnerability."}]}
            }
        ]
    },
    "anotherpackage": {
        "version": "2.3.4",
        "vulnerabilities": [
            {
                "CVE_data_meta": {"ID": "CVE-2023-5678"},
                "description": {"description_data": [{"value": "Another test vulnerability."}]}
            }
        ]
    }
}
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_dependency_alert_ai.py
```

## License

MIT License