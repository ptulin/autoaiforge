# AI Coding Workflow Automation

## Description
AI Coding Workflow Automation is a tool designed to streamline repetitive coding tasks by integrating AI coding assistants into custom workflows. It monitors file changes and triggers AI suggestions or improvements based on predefined configurations.

## Installation

Install the required dependencies:

```bash
pip install pyyaml watchdog pytest
```

## Usage

Run the tool with a configuration file:

```bash
python ai_coding_workflow_automation.py --config path/to/config.yml
```

## Configuration

The configuration file should be in YAML format and include triggers. Example:

```yaml
triggers:
  - type: file_change
    file: test.py
    ai_endpoint: http://mock-ai-endpoint.com
    instructions: Improve this code.
    action: log
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_coding_workflow_automation.py
```

## License

MIT License