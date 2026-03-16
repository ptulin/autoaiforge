# Contextual Memory Simulator

## Description
The Contextual Memory Simulator library allows developers to simulate context-sensitive memory systems. It helps test how well an AI agent integrates new information with existing memory, modeling scenarios like memory interference, forgetting, and reinforcement.

## Installation

```bash
pip install numpy==1.23.5 pytest==7.4.0
```

## Usage

```python
from contextual_memory_simulator import MemorySimulator

memory_state = np.array([0.5, 0.5, 0.5])
new_context = np.array([0.2, 0.3, 0.4])

result = MemorySimulator.simulate(memory_state, new_context)
print("Updated Memory State:", result["memory_state"])
print("Log:", result["log"])
```

## Features
- Simulates memory integration with reinforcement and decay mechanisms.
- Provides a modular API for testing memory interference and forgetting.
- Supports customizable parameters for reinforcement and decay.

## CLI Usage

```bash
python contextual_memory_simulator.py --memory_state "0.5,0.5,0.5" --new_context "0.2,0.3,0.4" --reinforcement_factor 1.5 --decay_factor 0.2
```

## License
MIT License
