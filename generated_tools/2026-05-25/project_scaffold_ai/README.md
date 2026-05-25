# Project Scaffold AI

## Overview

`project_scaffold_ai` is a Python-based automation tool that generates starter project structures and boilerplate code for various programming languages and frameworks. Developers can specify the type of project they want, and the tool will generate a ready-to-use directory structure and codebase.

## Features

- Generate project scaffolds for Python Flask applications.
- Support for optional features like authentication.
- Customizable output directory.

## Requirements

- Python 3.7+
- `jinja2` library
- `pytest` for running tests

Install dependencies using pip:

```bash
pip install jinja2 pytest
```

## Usage

Run the tool with the following command:

```bash
python project_scaffold_ai.py --language python --framework flask --features auth --output my_project
```

### Options

- `--language`: Programming language (currently only supports `python`).
- `--framework`: Framework (currently only supports `flask`).
- `--features`: Comma-separated list of features (e.g., `auth`).
- `--output`: Output directory for the generated project (default: `generated_project`).

## Running Tests

To run the tests, use the following command:

```bash
pytest test_project_scaffold_ai.py
```

All tests should pass without requiring network access.

## License

This project is licensed under the MIT License.