# Test Coverage Explainer

## Overview

`test_coverage_explainer` is a Python CLI tool that integrates with `coverage.py` to analyze test coverage reports and uses OpenAI's API to recommend areas in the codebase where test cases are missing or need improvement. It helps developers prioritize testing efforts based on critical code paths.

## Features

- Analyze test coverage reports in XML format.
- Identify uncovered lines in the code.
- Generate AI-driven suggestions for improving test coverage.
- Display results in a user-friendly table format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd test_coverage_explainer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Generate a coverage report in XML format using `coverage.py`:
   ```bash
   coverage run -m pytest
   coverage xml -o coverage.xml
   ```

2. Run the tool with the path to the coverage report:
   ```bash
   python test_coverage_explainer.py --report coverage.xml
   ```

3. View the uncovered lines and AI-generated suggestions in the console.

## Requirements

- Python 3.7+
- `rich`
- `openai`

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_test_coverage_explainer.py
```

All tests should pass successfully.

## Environment Variables

The tool requires an OpenAI API key to function. Set the `OPENAI_API_KEY` environment variable with your OpenAI API key:

```bash
export OPENAI_API_KEY=your_openai_api_key
```

## License

This project is licensed under the MIT License.