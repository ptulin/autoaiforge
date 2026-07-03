# Agent Simulation Tester

Agent Simulation Tester is a Python library that provides a simulation environment to test autonomous AI agents. Developers can simulate environments, define mock tasks or goals, and measure the performance of agents. This tool helps validate the robustness and effectiveness of agent workflows before deployment.

## Features
- Customizable simulation environments
- Performance metrics for agent behavior
- Supports multi-agent interactions

## Installation

Install the library and dependencies using pip:

```bash
pip install simpy==4.0.1 pandas==1.5.3 pytest==7.4.2
```

## Usage

### Example

```python
from agent_simulation_tester import Simulation

def agent(env, logs):
    while True:
        start_time = env.now
        yield env.timeout(5)  # Simulate agent work
        end_time = env.now
        logs.append({'type': 'agent', 'start_time': start_time, 'end_time': end_time})

def task(env, logs):
    while True:
        start_time = env.now
        yield env.timeout(10)  # Simulate task duration
        end_time = env.now
        logs.append({'type': 'task', 'start_time': start_time, 'end_time': end_time})

# Initialize simulation
env_config = {}
sim = Simulation(env_config)
sim.add_agent(agent)
sim.add_task(task)

# Run simulation
sim.run(until=50)

# Get performance metrics
metrics = sim.get_metrics()
print(metrics)
```

## Testing

Run the tests using pytest:

```bash
pytest test_agent_simulation_tester.py
```

## License

This project is licensed under the MIT License.