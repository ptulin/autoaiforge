# Agent Workflow Simulator

The Agent Workflow Simulator is a Python library and CLI tool that allows developers to simulate AI agent workflows before deploying them. It provides interactive feedback on agent decisions, logs, and potential bottlenecks, enabling rapid debugging and optimization of automation processes.

## Features

- Simulate agent workflows step-by-step.
- Log simulation details to a file or standard output.
- Identify potential bottlenecks and errors in workflows.

## Installation

Install the required dependencies using pip:

```
pip install click
```

## Usage

### CLI Usage

Run the tool from the command line:

```
python agent_workflow_simulator.py --workflow <path_to_workflow_file> [--log-file <path_to_log_file>]
```

- `--workflow`: Path to the workflow file (JSON format).
- `--log-file`: (Optional) Path to a log file to save simulation logs.

### Example Workflow File

```json
{
  "steps": [
    {"name": "Step 1", "action": "Action 1", "execution_time": 1},
    {"name": "Step 2", "action": "Action 2", "execution_time": 2}
  ]
}
```

### Library Usage

You can also use the simulator as a Python library:

```python
from agent_workflow_simulator import simulate_workflow

workflow = {
    "steps": [
        {"name": "Step 1", "action": "Action 1", "execution_time": 1},
        {"name": "Step 2", "action": "Action 2", "execution_time": 2}
    ]
}

simulate_workflow(workflow, log_file="simulation.log")
```

## Testing

To run the tests, install `pytest` and run:

```
pip install pytest
pytest test_agent_workflow_simulator.py
```

## License

This project is licensed under the MIT License.
