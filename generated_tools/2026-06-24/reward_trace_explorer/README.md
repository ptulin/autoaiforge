# Reward Trace Explorer

Reward Trace Explorer is a Python tool designed to help developers analyze how an AI agent's reward signals influence its decisions. It maps rewards to decision-making steps, allowing users to identify patterns, inconsistencies, or unexpected correlations in the behavior of reinforcement learning (RL) agents.

## Features

- Load data from CSV or JSON files.
- Analyze reward patterns and generate summary statistics.
- Visualize reward trends over time with a line plot.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas matplotlib
```

## Usage

Run the tool from the command line:

```bash
python reward_trace_explorer.py --input <path_to_input_file> --output <path_to_output_file>
```

- `--input`: Path to the input CSV or JSON file containing agent data. The file must have `step` and `reward` columns.
- `--output`: Path to save the output analysis graph.

### Example

```bash
python reward_trace_explorer.py --input agent_data.csv --output analysis_graph.png
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_reward_trace_explorer.py
```

The tests include:

- Verifying data loading from CSV and JSON files.
- Checking the correctness of reward analysis.
- Ensuring the reward plot is generated and saved correctly.

## License

This project is licensed under the MIT License.