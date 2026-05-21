# Multi-Agent Code Refactor Tool

## Overview

The Multi-Agent Code Refactor Tool is a Python library that utilizes multiple AI agents to collaboratively review and refactor Python code. Each agent specializes in a specific aspect, such as optimization, readability, or security. The agents work together to propose and implement comprehensive improvements to the input code.

## Features

- Supports multiple agents with different roles (e.g., style, performance, security).
- Accepts Python code as a string or from a file.
- Outputs refactored code and a detailed change report.
- Optionally saves the refactored code to a file.

## Installation

Install the required dependencies:

```bash
pip install pytest
```

## Usage

Run the tool from the command line:

```bash
python multi_agent_code_refactor.py "path_or_code" --agents style performance security --output_file output.py
```

- `path_or_code`: Path to the Python script or Python code as a string.
- `--agents`: List of agent roles (default: `style`, `performance`, `security`).
- `--output_file`: (Optional) Path to save the refactored code.

## Testing

Run the tests using `pytest`:

```bash
pytest test_multi_agent_code_refactor.py
```

## Notes

This tool uses mock implementations of AI agents for testing purposes. Replace the `review_code` method in `CodeRefactorAgent` with actual AI integration for production use.