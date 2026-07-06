# Context Graph Simulator

The Context Graph Simulator is a Python library that simulates AI agent behavior by replaying decisions stored in a context graph. It helps test how changes in past decisions or outcomes could influence future agent behavior, aiding in debugging and optimization.

## Features
- Simulate the impact of changing a node's outcome in a context graph.
- Visualize the graph and its updated state.
- Save the modified graph to a JSON file.

## Installation

Install the required dependencies using pip:

```bash
pip install networkx matplotlib pytest
```

## Usage

Run the script from the command line:

```bash
python context_graph_simulator.py --graph <path_to_graph_json> --node <node_id> --outcome <positive|neutral|negative> [--output <output_path>]
```

### Arguments
- `--graph`: Path to the serialized graph JSON file.
- `--node`: Node to modify.
- `--outcome`: New outcome for the node (`positive`, `neutral`, or `negative`).
- `--output`: (Optional) Path to save the modified graph JSON file.

### Example

```bash
python context_graph_simulator.py --graph example_graph.json --node decision_1 --outcome positive --output modified_graph.json
```

## Testing

Run the tests using pytest:

```bash
pytest test_context_graph_simulator.py
```

The tests include:
- Verifying the correct simulation of positive outcome changes.
- Verifying the correct simulation of negative outcome changes.
- Handling invalid node inputs gracefully.

## License

This project is licensed under the MIT License.