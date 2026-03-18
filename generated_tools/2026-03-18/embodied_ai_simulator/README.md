# Embodied AI Simulator

## Overview
The Embodied AI Simulator is a Python tool designed for simulating embodied AI environments with basic physics and 3D space. It allows developers to create virtual scenarios where AI agents can interact with objects, navigate spaces, and perform tasks. This provides a low-cost testing platform for embodied AI research and development.

## Features
- Simulates a virtual environment for embodied AI agents.
- Supports basic physics and interaction.
- Logs agent actions for analysis.
- Includes a simple graphical interface using Pygame.

## Requirements
- Python 3.7+
- `pygame`
- `numpy`
- `gym`

Install the required dependencies using pip:
```bash
pip install pygame numpy gym
```

## Usage
Run the simulator from the command line:
```bash
python embodied_ai_simulator.py --env warehouse --agent robot_arm --log logs.txt
```

### Arguments
- `--env`: Environment name (e.g., `warehouse`).
- `--agent`: Agent type (e.g., `robot_arm`).
- `--log`: (Optional) Path to save logs.

## Testing
The simulator includes a test suite written with `pytest`. To run the tests, install `pytest` and execute:
```bash
pip install pytest
pytest test_embodied_ai_simulator.py
```

The tests cover:
- Environment initialization.
- Simulation execution.
- Log saving functionality.

## License
This project is licensed under the MIT License.