# Autonomous Agent Debugger

## Overview
The Autonomous Agent Debugger is a Python tool designed to help developers debug autonomous AI agents. It allows you to trace decision paths, inspect intermediate data states, and identify bottlenecks in the agent's execution. The tool provides an interactive debugging interface tailored to AI workflows.

## Features
- Dynamically load and execute AI agent scripts.
- Interactive debugging interface with step-by-step execution.
- Error handling and traceback display for debugging issues.

## Installation
Install the required dependencies using pip:

```bash
pip install rich prompt_toolkit
```

## Usage
Run the tool from the command line:

```bash
python autonomous_agent_debugger.py --agent <path_to_agent_script> --task <task_input>
```

- `--agent`: Path to the Python script containing the AI agent. The script must define a callable `run_agent(task_input)` function.
- `--task`: Input task to provide to the agent.

## Example
Suppose you have an AI agent script `my_agent.py` with the following content:

```python
def run_agent(task_input):
    return f"Agent processed: {task_input}"
```

You can debug it using:

```bash
python autonomous_agent_debugger.py --agent my_agent.py --task "Test Task"
```

## Testing
Run the tests using pytest:

```bash
pytest test_autonomous_agent_debugger.py
```

The tests include:
- Valid agent loading.
- Handling missing agent files.
- Handling missing `run_agent` function.
- Interactive debugging functionality.

## License
This project is licensed under the MIT License.