# Multi-Agent Workload Balancer

## Description
The Multi-Agent Workload Balancer is a Python utility designed to optimize task assignments in multi-agent systems, such as Claude AI setups. It dynamically assigns tasks based on agent performance metrics and task complexity, ensuring efficient resource utilization and avoiding bottlenecks or idle agents.

## Features
- **Dynamic Task Assignment**: Assign tasks based on agent performance and task complexity.
- **Agent Health Checks**: Monitor agent load and health.
- **Configurable Policies**: Support for round-robin and priority-based balancing policies.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/multi_agent_workload_balancer.git
   cd multi_agent_workload_balancer
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool with a configuration file and specify the output file for task assignments:
```bash
python multi_agent_workload_balancer.py --config agent_config.yaml --output plan.json
```

### Example Configuration File (YAML)
```yaml
agents:
  - id: agent1
    name: Agent 1
  - id: agent2
    name: Agent 2

tasks:
  - id: task1
    complexity: 1
  - id: task2
    complexity: 2

policy: round-robin
```

## Testing
Run tests using pytest:
```bash
pytest test_multi_agent_workload_balancer.py
```

## License
MIT License
