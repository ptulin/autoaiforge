# Claude API Tester

## Overview
The `claude_api_tester` is a Python tool designed to help developers test and benchmark Anthropic's Claude Managed Agents APIs. It allows users to send different payloads, measure response times, and validate outputs against expected results. This tool is useful for ensuring the robustness of APIs in production environments.

## Features
- Send POST requests to a specified API endpoint with a JSON payload.
- Measure and display the response time.
- Validate the API response against an expected JSON output.
- Save the results (response and response time) to a file.

## Requirements
- Python 3.7+
- `httpx` library

Install the required dependencies using pip:
```bash
pip install httpx
```

## Usage
Run the tool from the command line with the following options:

```bash
python claude_api_tester.py --endpoint <API_ENDPOINT> --payload <PAYLOAD_FILE> [--expected <EXPECTED_FILE>] [--output <OUTPUT_FILE>]
```

### Arguments
- `--endpoint`: The URL of the API endpoint to test.
- `--payload`: Path to the JSON file containing the request payload.
- `--expected` (optional): Path to the JSON file containing the expected response.
- `--output` (optional): Path to save the results (response and response time).

### Example
```bash
python claude_api_tester.py --endpoint https://api.claude.ai --payload request.json --expected expected.json --output results.json
```

## Testing
The tool includes a test suite written with `pytest`. To run the tests, install `pytest` and run:

```bash
pip install pytest
pytest test_claude_api_tester.py
```

The tests cover the following scenarios:
1. Successful API request.
2. Failed API request due to a network error.
3. Validation of API response against expected output.

## Notes
- Ensure the API endpoint is accessible and the payload JSON file is correctly formatted.
- If the `--expected` argument is provided, the tool will validate the API response against the expected output.
- If the `--output` argument is provided, the tool will save the results to the specified file.
