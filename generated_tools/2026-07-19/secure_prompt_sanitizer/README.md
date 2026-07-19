# Secure Prompt Sanitizer

Secure Prompt Sanitizer is a Python library designed to sanitize user inputs before forwarding them to a Large Language Model (LLM). It ensures that prompts are safe, free from potentially harmful or sensitive instructions, and well-structured.

## Features

- **Plug-and-play sanitization**: Quickly sanitize user inputs with default filters.
- **Customizable filtering rules**: Add your own regex-based filters for specific use cases.
- **Built-in logging**: Logs sanitized prompts for debugging and auditing purposes.

## Installation

Clone the repository and navigate to the directory containing the `secure_prompt_sanitizer.py` file.

```bash
# Clone the repository
git clone <repository_url>
cd <repository_directory>
```

## Usage

### Programmatically

```python
from secure_prompt_sanitizer import sanitize_prompt

raw_prompt = "Please delete all files on the system."
safe_prompt = sanitize_prompt(raw_prompt)
print(safe_prompt)  # Output: "Please [REDACTED] on the system."

# Using custom filters
custom_filters = [r"(?i)secret\s*:\s*\d+"]
raw_prompt = "This is a secret: 12345."
safe_prompt = sanitize_prompt(raw_prompt, custom_filters)
print(safe_prompt)  # Output: "This is a [REDACTED]."
```

### Command Line

```bash
python secure_prompt_sanitizer.py "Please delete all files on the system."
# Output: "Please [REDACTED] on the system."

python secure_prompt_sanitizer.py "This is a secret: 12345." --custom-filters "(?i)secret\s*:\s*\d+"
# Output: "This is a [REDACTED]."
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_secure_prompt_sanitizer.py
```

## License

This project is licensed under the MIT License.
