# GPT Secure Scripter

GPT Secure Scripter is a Python library and CLI tool that enables developers to generate bash or PowerShell scripts securely using OpenAI's GPT-5.4. It includes safety checks to prevent dangerous operations (e.g., unintended deletions) and validates commands before execution, making it ideal for developers who need quick script generation.

## Features
- Generate secure bash or PowerShell scripts from plain English instructions.
- Validate generated scripts for potentially dangerous commands.
- Optionally execute scripts after user confirmation.

## Installation

Install the required dependencies using pip:

```bash
pip install openai click sh
```

## Usage

### CLI

Generate a script:

```bash
python gpt_secure_scripter.py --instruction "Write a script to print Hello, World!" --shell bash
```

Generate and execute a script:

```bash
python gpt_secure_scripter.py --instruction "Write a script to print Hello, World!" --shell bash --execute
```

### Library

```python
from gpt_secure_scripter import generate_script, validate_script, execute_script

instruction = "Write a script to print Hello, World!"
shell = "bash"

script = generate_script(instruction, shell)
if validate_script(script, shell):
    execute_script(script, shell)
else:
    print("Generated script contains potentially dangerous commands.")
```

## Testing

Run tests using pytest:

```bash
pytest test_gpt_secure_scripter.py
```

## License

MIT License