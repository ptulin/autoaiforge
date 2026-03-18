# Agent Simulation Sandbox

## Overview
This CLI tool provides a sandbox environment to test autonomous AI agents in simulated task scenarios. Developers can create and execute mock environments to evaluate the agent's decision-making processes and task execution before real-world deployment.

## Installation

Install the required dependencies using pip:

```bash
pip install gym click matplotlib
```

## Usage

Run the CLI tool with the following options:

```bash
python agent_simulation_sandbox.py --config <path_to_config.json> --agent <path_to_agent.py>
```

### Options

- `--config`: Path to the scenario configuration file (JSON format).
- `--agent`: Path to the agent script (Python file).

## Example

1. Create a JSON configuration file (e.g., `scenario.json`):

```json
{
  "environment": "CartPole-v1",
  "max_steps": 500
}
```

2. Create an agent script (e.g., `agent.py`):

```python
class Agent:
    def act(self, observation):
        return 0  # Example action
```

3. Run the simulation:

```bash
python agent_simulation_sandbox.py --config scenario.json --agent agent.py
```

## Testing

Run the tests using pytest:

```bash
pytest test_agent_simulation_sandbox.py
```

## License

This project is licensed under the MIT License.
