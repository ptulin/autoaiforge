# Dynamic Behavior Analyzer

## Description
Dynamic Behavior Analyzer is a Python tool designed to execute AI scripts in a controlled sandbox environment. It monitors runtime behaviors such as API calls, file operations, and memory usage to identify potentially suspicious or undocumented operations. The tool is particularly useful for detecting features like "Undercover Mode" by analyzing input-output patterns and logging behaviors.

## Features
- **Secure Sandbox Execution**: Runs scripts in an isolated environment to prevent unintended side effects.
- **Behavior Monitoring**: Tracks memory usage, output patterns, and suspicious keywords.
- **Detailed Reports**: Generates a JSON report summarizing runtime behaviors and flagged patterns.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/dynamic_behavior_analyzer.git
   cd dynamic_behavior_analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python dynamic_behavior_analyzer.py --script <path_to_script> --output <path_to_report> [--args <script_arguments>]
```

### Example

```bash
python dynamic_behavior_analyzer.py --script ./ai_script.py --output behavior_report.json --args --mode test
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_dynamic_behavior_analyzer.py
```

## Limitations
- The tool does not provide full system call tracing.
- It relies on keyword-based detection for suspicious patterns, which may result in false positives or negatives.

## License
This project is licensed under the MIT License.