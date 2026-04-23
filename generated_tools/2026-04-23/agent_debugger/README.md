# Agent Debugger

## Description
Agent Debugger is a Python CLI tool designed to help developers debug autonomous AI agents by simulating task flows and inspecting decision-making processes. It provides step-by-step insights into agent behavior and generates visual graphs to represent task flows and dependencies.

## Features
- Simulate task execution without real-world effects
- Inspect intermediate agent states and decisions
- Generate visual graphs for task flows and dependencies

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd agent_debugger
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool with the following command:
```bash
python agent_debugger.py --config <path_to_config_file> --output <output_image_path>
```

### Example
Given a configuration file `agent_config.json`:
```json
{
  "tasks": [
    {"id": "task1", "name": "Task 1", "dependencies": []},
    {"id": "task2", "name": "Task 2", "dependencies": ["task1"]}
  ]
}
```
Run the tool:
```bash
python agent_debugger.py --config agent_config.json --output task_flow.png
```
This will generate a graph image `task_flow.png` visualizing the task flow.

## Testing
Run the tests using pytest:
```bash
pytest test_agent_debugger.py
```

## Requirements
- Python 3.8+
- networkx==3.1
- matplotlib==3.8.0

## License
MIT License