# Decision Audit Tool

## Overview
The Decision Audit Tool is an automation utility designed to audit decision logs from AI models used in military simulations. It parses logs, identifies potential ethical violations, and flags decisions that may require human review.

## Features
- Load ethical rules from a YAML file.
- Parse decision logs from CSV or JSON files.
- Audit decisions based on ethical rules.
- Save flagged decisions to CSV or JSON files.

## Installation
Install the required dependencies using pip:

```bash
pip install pandas pyyaml
```

## Usage
Run the tool from the command line:

```bash
python decision_audit_tool.py --log <path_to_log_file> --rules <path_to_rules_file> [--output <path_to_output_file>]
```

### Arguments
- `--log`: Path to the AI decision log file (CSV or JSON).
- `--rules`: Path to the YAML file containing ethical rules.
- `--output`: Optional path to save flagged decisions (CSV or JSON).

### Example
```bash
python decision_audit_tool.py --log decisions.csv --rules rules.yaml --output flagged_decisions.csv
```

## Testing
Run the tests using pytest:

```bash
pytest test_decision_audit_tool.py
```

## License
This tool is provided under the MIT License.