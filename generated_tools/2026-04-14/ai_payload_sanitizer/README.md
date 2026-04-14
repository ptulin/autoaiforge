# AI Payload Sanitizer

## Description
AI Payload Sanitizer is a Python library designed to sanitize potentially unsafe user inputs before sending them to AI APIs, reducing the risk of injection attacks or unintended behavior. It applies customizable rules for filtering and sanitization.

## Features
- Prevents injection attacks and malicious payloads.
- Customizable sanitization rules for text or JSON inputs.
- Handles nested JSON payloads.
- Logs sanitized inputs and original payloads for debugging.

## Installation
No external dependencies are required. Simply download the `ai_payload_sanitizer.py` file and include it in your project.

## Usage
```python
from ai_payload_sanitizer import sanitize

# Example 1: Sanitize a string
input_data = "DROP DATABASE"
print(sanitize(input_data))  # Output: [REDACTED]

# Example 2: Sanitize a JSON payload
input_data = {"query": "DROP DATABASE", "safe": "SELECT *"}
print(sanitize(input_data))

# Example 3: Custom sanitization rules
rules = {r"(?i)delete\s+from": "REMOVED"}
input_data = "DELETE FROM users"
print(sanitize(input_data, rules))  # Output: REMOVED users
```

## CLI Usage
You can also use the tool via the command line:
```bash
python ai_payload_sanitizer.py '{"query": "DROP DATABASE"}'
```

## License
This project is licensed under the MIT License.