# Agent Collaboration Simulator

## Description
The Agent Collaboration Simulator is a Python-based CLI tool that simulates collaboration between multiple AI agents in a controlled environment. It allows developers to test how agents interact, share data, and resolve conflicts when working collaboratively. The tool provides real-time logging and optional visualization of agent interactions.

## Features
- Simulate collaboration between multiple agents.
- Define agents, tasks, and communication rules via JSON or YAML configuration files.
- Real-time logging of agent interactions and task assignments.
- Optional visualization of the agent collaboration network.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with a configuration file:
```bash
python agent_collaboration_simulator.py --config agents_config.yml
```

To enable visualization of the agent collaboration network:
```bash
python agent_collaboration_simulator.py --config agents_config.yml --visualize
```

## Configuration File Format
The configuration file can be in JSON or YAML format. Below is an example of a YAML configuration file:

```yaml
agents:
  - name: Agent1
  - name: Agent2

tasks:
  - name: Task1
    assigned_to: Agent1

communication:
  - from: Agent1
    to: Agent2
    type: message
```

## Example Output

```
Task 'Task1' assigned to agent 'Agent1'.
```

If visualization is enabled, a graph of the agent collaboration network will be displayed.

## Testing

Run the tests using pytest:
```bash
pytest test_agent_collaboration_simulator.py
```

## License
This project is licensed under the MIT License.