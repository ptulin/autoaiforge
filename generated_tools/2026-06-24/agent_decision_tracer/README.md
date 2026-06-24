# Agent Decision Tracer

## Overview
The Agent Decision Tracer is a Python tool designed to trace the step-by-step decision-making process of AI agents. It captures intermediate states, decisions, and associated reasoning at each step, helping developers debug complex agent behaviors by visualizing their execution paths in a clear and structured format.

## Features
- Load decision logs from a JSON file or stdin.
- Validate the structure of decision logs.
- Generate a visual execution graph in `.dot` or `.png` format.
- Optionally save structured trace logs as JSON.

## Installation
Install the required Python package:

```bash
pip install graphviz
```

## Usage
Run the tool from the command line:

```bash
python agent_decision_tracer.py --input <input_file_or_dash> --output <output_file> [--log <log_file>]
```

### Arguments
- `--input`: Path to the JSON file containing decision logs. Use `-` to read from stdin.
- `--output`: Path to save the output graph (e.g., `output.dot` or `output.png`).
- `--log` (optional): Path to save the structured trace logs as JSON.

## Example
Input JSON file (`input.json`):

```json
[
    {"step": 1, "decision": "start", "reasoning": "initialization"},
    {"step": 2, "decision": "move", "reasoning": "next step", "previous_step": 1}
]
```

Command:

```bash
python agent_decision_tracer.py --input input.json --output output_graph.png --log trace_logs.json
```

Output:
- `output_graph.png`: A visual representation of the execution graph.
- `trace_logs.json`: The structured trace logs.

## Testing
Run the tests using `pytest`:

```bash
pytest test_agent_decision_tracer.py
```

The tests include:
- Loading decision logs from a file.
- Loading decision logs from stdin.
- Validating decision logs.
- Generating an execution graph.

## License
MIT License