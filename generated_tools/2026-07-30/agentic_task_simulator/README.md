# Agentic Task Simulator

## Description
The Agentic Task Simulator is a CLI tool designed to simulate and debug AI agent workflows in a sandboxed environment. By running agents with predefined inputs and outputs, developers can identify bottlenecks and improve task orchestration before deployment.

## Features
- Mock environment setup for AI agents
- Predefined input/output simulation
- Debugging visualization for workflows

## Installation
```bash
pip install matplotlib==3.7.1
```

## Usage
```bash
python agentic_task_simulator.py --agents agent1.py agent2.py --scenario scenario.json --visualize
```

### Arguments
- `--agents`: Paths to agent scripts to simulate (required).
- `--scenario`: Path to the JSON scenario file (required).
- `--visualize`: Optional flag to visualize the simulation metrics.

## Example
```bash
python agentic_task_simulator.py --agents agent1.py agent2.py --scenario scenario.json
```

## Output
- Simulation logs printed to the console.
- Debug metrics displayed as JSON.
- Optional visualization of metrics as a bar chart.

## License
This project is licensed under the MIT License.