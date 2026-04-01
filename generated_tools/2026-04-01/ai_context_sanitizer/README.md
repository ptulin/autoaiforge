# AI Context Sanitizer

## Overview

The AI Context Sanitizer is a Python utility designed to sanitize user inputs and prompts before sending them to AI models like ChatGPT. This helps prevent unintended behavior or exploitation through malicious prompt crafting.

## Features

- Removes system-level commands from prompts.
- Supports custom sanitization rules via a YAML configuration file.
- Handles edge cases like missing or invalid configuration files.

## Installation

Install the required dependencies using pip:

```bash
pip install pyyaml
```

## Usage

### Command Line Interface

Run the script directly from the command line:

```bash
python ai_context_sanitizer.py "Your prompt here" --config path/to/config.yaml
```

- `prompt`: The raw user input or prompt string to sanitize.
- `--config`: (Optional) Path to a YAML configuration file containing custom sanitization rules.

### Example YAML Configuration

```yaml
rules:
  - pattern: "test"
    replacement: "mock"
```

### Programmatic Usage

You can also use the utility functions directly in your Python code:

```python
from ai_context_sanitizer import sanitize_prompt, load_config

config = load_config("path/to/config.yaml")
prompt = "This is a test prompt"
sanitary_prompt = sanitize_prompt(prompt, config)
print(sanitary_prompt)
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_context_sanitizer.py
```

## License

This project is licensed under the MIT License.
