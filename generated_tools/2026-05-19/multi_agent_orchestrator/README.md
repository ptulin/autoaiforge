# Multi-Agent Orchestrator

## Description
The Multi-Agent Orchestrator is a Python library designed to help developers create, configure, and manage multiple AI coding agents working on interdependent tasks. It provides tools to define agent roles, facilitate inter-agent communication, and monitor task progress, making it ideal for collaborative or multi-step coding workflows.

## Features
- Define and manage multiple AI agents with distinct roles.
- Built-in support for inter-agent communication via pub/sub.
- Event-driven architecture to handle task dependencies.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

1. Create a configuration JSON file (e.g., `config.json`):

```json
{
    "agents": [
        {"name": "Agent1", "role": "Developer", "tasks": ["Task1", "Task2"]},
        {"name": "Agent2", "role": "Reviewer", "tasks": ["Task3"]}
    ]
}
```

2. Run the orchestrator:

```bash
python multi_agent_orchestrator.py --config config.json
```

## Example Output

```
[Agent1] Completed task 'Task1': Simulated response for Task1 by Developer
[Agent1] Completed task 'Task2': Simulated response for Task2 by Developer
[Agent2] Completed task 'Task3': Simulated response for Task3 by Reviewer
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_multi_agent_orchestrator.py
```

## License
This project is licensed under the MIT License.
