# Safe Command Validator

## Overview

The Safe Command Validator is a Python tool designed to validate system-level commands against a predefined whitelist or blacklist. This ensures that unauthorized or dangerous commands are not executed, providing an additional layer of safety in production environments.

## Features

- Validate commands against a whitelist (allowed commands).
- Validate commands against a blacklist (disallowed commands).
- Handle missing or invalid rules files gracefully.
- Log warnings and errors for better debugging.

## Installation

This tool requires Python 3.6 or later. No additional packages are required as it uses only the Python standard library.

## Usage

Run the tool from the command line:

```bash
python safe_command_validator.py <command> <rules_file>
```

- `<command>`: The command string to validate.
- `<rules_file>`: Path to the JSON file containing whitelist/blacklist rules.

### Example

```bash
python safe_command_validator.py "ls -la" "rules.json"
```

## Rules File Format

The rules file should be a JSON file with the following structure:

```json
{
  "whitelist": ["^ls", "^echo"],
  "blacklist": ["rm -rf", "shutdown"]
}
```

- `whitelist`: A list of regular expressions defining allowed commands.
- `blacklist`: A list of regular expressions defining disallowed commands.

## Testing

The tool includes a comprehensive test suite using `pytest`. To run the tests:

```bash
pytest test_safe_command_validator.py
```

## License

This project is licensed under the MIT License.