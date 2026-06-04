# Local Privacy Guard for LLMs

## Description
Local Privacy Guard is a Python library designed to monitor and intercept communication between a user and a local LLM instance. It ensures that sensitive data is not leaked by analyzing outgoing text and applying predefined or custom privacy rules. The tool flags data leakage risks in real-time, providing warnings or blocking operations entirely.

## Features
- Middleware to intercept and analyze outgoing LLM data.
- Support for predefined or custom privacy rules.
- Alerting and blocking mechanisms for sensitive data.
- Simple function wrapping for seamless integration.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
### Example
```python
from local_privacy_guard import PrivacyGuard

# Initialize PrivacyGuard with rules
guard = PrivacyGuard(rules=[r'\bpassword\b', r'\bsecret\b'])

# Check text for sensitive data
try:
    sanitized_text = guard.check("This is a test with password.")
except ValueError as e:
    print(e)

# Wrap a function to intercept its input
@guard.wrap
def example_function(input_text):
    return f"Processed: {input_text}"

try:
    result = example_function("This contains secret information.")
except ValueError as e:
    print(e)
```

## Testing
Run tests using pytest:
```bash
pytest test_local_privacy_guard.py
```

## License
MIT License