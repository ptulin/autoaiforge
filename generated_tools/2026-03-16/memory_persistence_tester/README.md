# Memory Persistence Tester

## Description
The Memory Persistence Tester is a CLI tool designed to simulate and evaluate memory persistence in AI agents. It emulates various memory storage and retrieval strategies, allowing developers to benchmark how well an AI model retains and utilizes contextual information over time across sessions.

## Features
- Simulates multiple memory strategies: short-term, long-term, episodic
- Configurable memory decay rates and retrieval algorithms
- Generates detailed performance reports with metrics like recall accuracy

## Installation

```bash
pip install numpy==1.24.2 matplotlib==3.7.1
```

## Usage

### CLI Arguments
- `--tasks`: Number of tasks to simulate (required)
- `--decay_rate`: Memory decay rate (0-1) (required)
- `--strategy`: Memory strategy (`short-term`, `long-term`, `episodic`) (required)
- `--report`: Generate graphical report (optional)

### Example

```bash
python memory_persistence_tester.py --tasks 100 --decay_rate 0.1 --strategy 'episodic' --report
```

## Output
- Console output showing simulation results
- Optional graphical report displaying memory performance metrics

## Testing
Run the tests using pytest:

```bash
pytest test_memory_persistence_tester.py
```