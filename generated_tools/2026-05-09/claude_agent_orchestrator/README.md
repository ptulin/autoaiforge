# Claude Agent Orchestrator

The Claude Agent Orchestrator is a Python-based tool that allows developers to efficiently manage, monitor, and optimize multiple Claude AI agents working on collaborative tasks. It provides a CLI for orchestrating workflows, setting task dependencies, and visualizing agent interactions in real-time.

## Features
- Load workflows from YAML or JSON configuration files.
- Visualize tasks and their dependencies in a tabular format.
- Execute tasks in the correct order based on dependencies.
- Log task execution details to a file (optional).

## Installation

Install the required dependencies using pip:

```bash
pip install rich pyyaml networkx
```

## Usage

Run the orchestrator with the following command:

```bash
python claude_agent_orchestrator.py --workflow <path_to_workflow_file> [--log <path_to_log_file>]
```

### Arguments
- `--workflow`: Path to the workflow configuration file (YAML or JSON format).
- `--log`: (Optional) Path to the log file for recording task execution details.

## Workflow File Format

The workflow file should be in either YAML or JSON format and follow this structure:

```yaml
tasks:
  task1:
    status: "pending"
    dependencies: []
  task2:
    status: "pending"
    dependencies: ["task1"]
```

### Example JSON File

```json
{
  "tasks": {
    "task1": {"status": "pending", "dependencies": []},
    "task2": {"status": "pending", "dependencies": ["task1"]}
  }
}
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests with:

```bash
pytest test_claude_agent_orchestrator.py
```

## License

This project is licensed under the MIT License.