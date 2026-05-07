# Adaptive Agent Scheduler

## Overview

The Adaptive Agent Scheduler is a Python CLI tool designed to dynamically schedule tasks for multiple AI agents based on workload, priority, and agent availability. It uses heuristics and basic machine learning to ensure task allocation is optimized for efficiency and fairness.

## Features

- Load tasks and agents data from CSV files.
- Dynamically schedule tasks to agents based on priority and availability.
- Save the generated schedule to a CSV or JSON file.

## Requirements

- Python 3.7+
- pandas
- scikit-learn

## Installation

Install the required dependencies:

```bash
pip install pandas scikit-learn
```

## Usage

Run the tool from the command line:

```bash
python adaptive_agent_scheduler.py --tasks <tasks_csv_path> --agents <agents_csv_path> --output <output_file>
```

### Arguments

- `--tasks`: Path to the tasks CSV file.
- `--agents`: Path to the agents CSV file.
- `--output`: Path to the output file (must be `.csv` or `.json`).

## Example

```bash
python adaptive_agent_scheduler.py --tasks tasks.csv --agents agents.csv --output schedule.json
```

## Testing

Run the tests using pytest:

```bash
pytest test_adaptive_agent_scheduler.py
```

## License

This project is licensed under the MIT License.