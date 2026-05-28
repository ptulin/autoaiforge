# Sandboxed Vulnerability Playground

## Overview

The Sandboxed Vulnerability Playground is a Python tool designed to create a local sandboxed environment where Python scripts can be executed safely. It also allows for the simulation of security vulnerabilities using LLM-generated prompts. This tool is useful for developers and researchers aiming to understand the capabilities of LLMs in generating and reproducing vulnerabilities in a controlled environment.

## Features

- Execute Python scripts in a sandboxed environment.
- Inject LLM-generated vulnerabilities into scripts for testing purposes.
- Safely handle errors and ensure isolation of the execution environment.

## Requirements

- Python 3.7+

## Installation

No additional dependencies are required. Simply clone this repository and run the script.

```bash
git clone <repository_url>
cd sandboxed_vuln_playground
python sandboxed_vuln_playground.py --help
```

## Usage

To execute a Python script in the sandbox:

```bash
python sandboxed_vuln_playground.py --script <path_to_script>
```

To execute a Python script with an LLM-generated vulnerability prompt:

```bash
python sandboxed_vuln_playground.py --script <path_to_script> --llm_prompt "<your_prompt>"
```

## Testing

To run the tests, install `pytest` and execute the following command:

```bash
pytest test_sandboxed_vuln_playground.py
```

The tests ensure that the tool handles various scenarios, including:

1. Running a script without an LLM prompt.
2. Running a script with an LLM prompt.
3. Handling missing script files gracefully.

## License

This project is licensed under the MIT License.