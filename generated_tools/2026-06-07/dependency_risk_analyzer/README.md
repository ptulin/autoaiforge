# Dependency Risk Analyzer

## Overview
The Dependency Risk Analyzer is a Python tool that analyzes the dependencies in your Python project for known vulnerabilities. It uses an AI model to classify security risks and cross-references dependency versions with public vulnerability databases like CVE. The tool outputs a risk report in either JSON or Markdown format.

## Features
- Parses `requirements.txt` or `pyproject.toml` files to extract dependencies.
- Queries the CVE database for known vulnerabilities.
- Uses an AI model to classify the risk level of each vulnerability.
- Outputs a detailed risk report in JSON or Markdown format.

## Installation

Install the required dependencies:

```bash
pip install requests pandas transformers toml
```

## Usage

Run the tool with the following command:

```bash
python dependency_risk_analyzer.py <file_path> --output-format <json|markdown>
```

- `<file_path>`: Path to your `requirements.txt` or `pyproject.toml` file.
- `--output-format`: Output format for the risk report. Options are `json` or `markdown`. Default is `json`.

### Example

```bash
python dependency_risk_analyzer.py requirements.txt --output-format markdown
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests using:

```bash
pytest test_dependency_risk_analyzer.py
```

## Limitations
- Requires an internet connection to query the CVE database.
- The AI model used for risk classification may not be 100% accurate.

## License

This project is licensed under the MIT License.