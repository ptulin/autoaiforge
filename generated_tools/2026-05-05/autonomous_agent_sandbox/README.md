# Autonomous Agent Sandbox

The Autonomous Agent Sandbox is a Python-based CLI tool designed to provide a controlled environment for safely testing and simulating autonomous AI agents. Developers can define agent behaviors, environmental constraints, and test scenarios to evaluate agent performance before deploying them in production.

## Features
- Load simulation scenarios from JSON or YAML files.
- Load agent logic from Python files.
- Simulate agent behavior in OpenAI Gym environments.
- Save simulation results to a CSV file.

## Installation

Install the required dependencies:

```bash
pip install typer gym pandas pyyaml
```

## Usage

Run the CLI tool with the following command:

```bash
python autonomous_agent_sandbox.py --scenario <scenario_file> --agent <agent_file> [--output <output_file>]
```

### Arguments
- `--scenario`: Path to the JSON or YAML file defining the simulation scenario.
- `--agent`: Path to the Python file containing the agent logic.
- `--output` (optional): Path to save the simulation results as a CSV file.

### Example

```bash
python autonomous_agent_sandbox.py --scenario scenario.json --agent agent.py --output results.csv
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_autonomous_agent_sandbox.py
```

The tests include:
- Loading scenarios from JSON and YAML files.
- Loading agent logic from a Python file.
- Running a simulation with a mock environment and agent.

## License

This project is licensed under the MIT License.