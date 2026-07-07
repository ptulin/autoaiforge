# Local AI Workspace Validator

## Overview

The Local AI Workspace Validator is a Python-based tool designed to ensure that local AI workspaces are correctly configured for hybrid workflows. It checks for:

- Missing dependencies
- Hardware compatibility (e.g., GPU/CPU)
- Proper configuration of local and remote endpoints

This tool assists developers in troubleshooting and validating their AI workspace environments.

## Installation

Install the required dependencies using pip:

```bash
pip install psutil requests
```

## Usage

Run the tool using the command line:

```bash
python local_ai_workspace_validator.py --workspace /path/to/workspace --output /path/to/report.json
```

### Arguments

- `--workspace`: Path to the AI workspace.
- `--output`: (Optional) Path to save the validation report as a JSON file.

## Example

```bash
python local_ai_workspace_validator.py --workspace ./my_workspace --output ./report.json
```

## Testing

Run the tests using pytest:

```bash
pytest test_local_ai_workspace_validator.py
```

## License

MIT License
