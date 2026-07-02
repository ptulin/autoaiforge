# Code Review Simulator

## Overview

The Code Review Simulator is a CLI tool that generates synthetic pull requests based on user-defined templates and evaluates AI agents on their ability to perform code reviews. It provides feedback, identifies bugs, and suggests improvements.

## Features

- Load pull request templates and agent feedback from JSON or YAML files.
- Validate agent feedback against a JSON schema.
- Evaluate feedback accuracy and display results in a formatted table or JSON.

## Installation

Install the required dependencies:

```bash
pip install typer rich jsonschema pyyaml
```

## Usage

Run the tool using the following command:

```bash
python code_review_simulator.py --pr-template <path_to_template> --agent-feedback <path_to_feedback> --schema-file <path_to_schema> [--output-json]
```

### Arguments

- `--pr-template`: Path to the pull request template file (JSON or YAML).
- `--agent-feedback`: Path to the agent feedback file (JSON).
- `--schema-file`: Path to the JSON schema for validating agent feedback.
- `--output-json`: Optional flag to output results as JSON instead of a table.

## Testing

Run tests using pytest:

```bash
pytest test_code_review_simulator.py
```

## License

This project is licensed under the MIT License.