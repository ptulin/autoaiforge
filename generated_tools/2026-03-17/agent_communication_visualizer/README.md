# Agent Communication Visualizer

## Overview
The Agent Communication Visualizer is a CLI tool for visualizing communication flows between agents in multi-agent systems. It reads log files containing agent interactions, analyzes message flows, and generates communication graphs to identify collaboration bottlenecks and inefficiencies.

## Features
- Parse log files to extract communication flows.
- Generate directed graphs to visualize agent interactions.
- Save the generated graphs as PNG files.

## Installation
Install the required Python packages using pip:

```bash
pip install networkx matplotlib
```

## Usage
Run the tool from the command line:

```bash
python agent_communication_visualizer.py --logs <path_to_log_file> --output <path_to_output_png>
```

### Arguments
- `--logs`: Path to the log file containing agent communication data. Each line in the file should be in the format `sender,receiver`.
- `--output`: Path to save the generated communication graph PNG file.

## Example
Given a log file `logs.txt` with the following content:

```
agent1,agent2
agent2,agent3
agent3,agent1
```

Run the tool:

```bash
python agent_communication_visualizer.py --logs logs.txt --output communication_graph.png
```

This will generate a graph showing the communication flows between the agents and save it as `communication_graph.png`.

## Testing
Run the tests using pytest:

```bash
pytest test_agent_communication_visualizer.py
```

## License
This project is licensed under the MIT License.