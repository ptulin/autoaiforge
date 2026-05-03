# Recursive Agent Debugger

This tool allows AI developers to step through and visualize the recursive decision-making process of self-improving AI agents. It monitors how agents evolve their logic over iterations and provides debugging hooks to inspect state changes, decision trees, and improvement metrics.

## Features
- Load and debug custom AI agent classes.
- Visualize the decision-making process as a graph.
- Display performance metrics in a tabular format.

## Installation

Install the required dependencies:

```bash
pip install networkx matplotlib rich
```

## Usage

Run the tool with the following command:

```bash
python recursive_agent_debugger.py --agent_file <path_to_agent_file> --steps <number_of_steps>
```

- `--agent_file`: Path to the Python file containing the `Agent` class.
- `--steps`: Number of recursive iterations to debug (default: 10).

## Testing

Run the tests using `pytest`:

```bash
pytest test_recursive_agent_debugger.py
```

## Example

Suppose you have an `agent.py` file with the following content:

```python
class Agent:
    def __init__(self):
        self.state = 0

    def get_state(self):
        return self.state

    def make_decision(self):
        return f"decision_{self.state}"

    def improve_logic(self):
        self.state += 1
        return f"improvement_{self.state}"
```

Run the debugger as follows:

```bash
python recursive_agent_debugger.py --agent_file agent.py --steps 5
```

This will visualize the decision tree and display the performance metrics.