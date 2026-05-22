# AI Agent Test Harness

## Overview

`ai_agent_test_harness` is a Python CLI tool designed to automate the testing of AI agent workflows. It simulates predefined input scenarios, compares the outputs against expected results, and generates a summary report. The tool integrates with LangSmith and Claude Code to validate agent behavior across edge cases, logging discrepancies for easier debugging.

## Features

- Load test configurations from a YAML file.
- Simulate test cases by sending HTTP POST requests to specified endpoints.
- Compare actual outputs with expected outputs.
- Generate a summary report of test results, including pass/fail status and details.
- Optional integration with LangSmith API using an API key.

## Requirements

- Python 3.7+
- `pyyaml`
- `rich`
- `requests`
- `pytest` (for testing)

## Installation

Install the required dependencies using pip:

```bash
pip install pyyaml rich requests pytest
```

## Usage

Run the CLI tool with the following arguments:

```bash
python ai_agent_test_harness.py --test_config <path_to_yaml_config> --output <path_to_output_log> [--langsmith_api_key <api_key>]
```

- `--test_config`: Path to the YAML file containing test configurations.
- `--output`: Path to the output log file where the test summary will be saved.
- `--langsmith_api_key`: (Optional) API key for LangSmith integration.

## Example

Create a YAML configuration file `test_config.yaml`:

```yaml
test_cases:
  - name: Test Case 1
    endpoint: http://example.com/api
    input:
      key: value
    expected_output:
      result: success
```

Run the tool:

```bash
python ai_agent_test_harness.py --test_config test_config.yaml --output test_results.log
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_ai_agent_test_harness.py
```

The test suite includes:

1. Testing the loading of YAML test configurations.
2. Testing the success and failure of test cases.
3. Testing the generation of the summary report.

## License

This project is licensed under the MIT License.