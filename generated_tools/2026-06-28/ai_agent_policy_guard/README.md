# AI Agent Policy Guard

AI Agent Policy Guard is a Python-based governance tool that monitors and enforces behavior policies for autonomous AI agents. It allows developers to define policy rules in YAML or JSON, and the tool continuously audits agent actions, ensuring compliance. If violations are detected, it can log, alert, or halt execution.

## Features

- Load policy rules from YAML or JSON files.
- Validate policy structure using JSON Schema.
- Monitor logs in real-time for policy violations.
- Perform actions (log, alert, halt) based on policy violations.

## Installation

Install the required dependencies using pip:

```bash
pip install jsonschema pyyaml colorlog
```

## Usage

Run the tool with the following command:

```bash
python ai_agent_policy_guard.py --policy <path_to_policy_file> --log <path_to_log_file>
```

- `--policy`: Path to the policy file (YAML or JSON format).
- `--log`: Path to the log file to monitor, or use `-` to read from standard input.

## Example

### Policy File (YAML)

```yaml
rules:
  - pattern: "error"
    action: "log"
  - pattern: "critical"
    action: "halt"
```

### Log File

```
This is an error message
This is a critical issue
```

### Command

```bash
python ai_agent_policy_guard.py --policy policy.yaml --log logs.txt
```

## Testing

To run the tests, install `pytest` and execute the test file:

```bash
pip install pytest
pytest test_ai_agent_policy_guard.py
```

The test suite includes tests for loading policies, validating policies, and monitoring logs for policy violations.
