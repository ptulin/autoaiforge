# Memory Decay Simulator

## Overview
The Memory Decay Simulator is a Python-based CLI tool designed to simulate and visualize memory decay in AI systems. It supports two decay strategies: exponential and linear. Users can test different decay rates and durations to analyze how memory diminishes over time.

## Features
- Simulate exponential and linear memory decay.
- Visualize memory decay using matplotlib.
- Save the decay plot as an image file.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd memory_decay_simulator
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the CLI tool with the following arguments:

```bash
python memory_decay_simulator.py --strategy <strategy> --rate <rate> --duration <duration>
```

### Arguments
- `--strategy`: Decay strategy (`exponential` or `linear`).
- `--rate`: Decay rate (positive float).
- `--duration`: Duration of the simulation (positive integer).

### Example
Simulate exponential decay with a rate of 0.05 over 100 time units:

```bash
python memory_decay_simulator.py --strategy exponential --rate 0.05 --duration 100
```

## Testing
Run the tests using pytest:

```bash
pytest test_memory_decay_simulator.py
```

## License
This project is licensed under the MIT License.