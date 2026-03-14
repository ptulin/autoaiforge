# Silo Audit Tool

## Overview
The Silo Audit Tool is a Python utility designed to audit and monitor encrypted data silos in AI workflows. It logs and reports access events, failed access attempts, and performs encryption integrity checks to ensure transparency and compliance in data usage.

## Features
- Logs access events and failed access attempts.
- Performs SHA-256 integrity checks on encrypted data silos.
- Generates audit reports in JSON format.

## Requirements
- Python 3.7+
- `cryptography` library

Install the required Python package using pip:
```
pip install cryptography
```

## Usage
Run the tool from the command line with the following options:

```
python silo_audit_tool.py --silo <path_to_silo> [--loglevel <level>] [--report <format>]
```

### Arguments
- `--silo`: Path to the encrypted data silo (required).
- `--loglevel`: Logging level (default: `INFO`). Options: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
- `--report`: Format of the audit report (default: `json`). Currently, only `json` is supported.

### Example
```
python silo_audit_tool.py --silo data.silo --loglevel DEBUG --report json
```

## Testing
The tool includes a test suite using `pytest`. To run the tests, install `pytest`:

```
pip install pytest
```

Run the tests with:

```
pytest test_silo_audit_tool.py
```

The tests include mocking for file operations and do not require network access.
