# Context Graph Builder

## Description
Context Graph Builder is a Python library for creating and managing context graphs that store AI agent decisions and their outcomes. This helps developers improve agent memory by enabling retrieval and analysis of past interactions.

## Features
- Create graph nodes for decisions and outcomes
- Flexible querying of stored context data
- Graph visualization for debugging and insights

## Installation

Install the required dependencies using pip:

```bash
pip install networkx==3.1 matplotlib==3.7.2
```

## Usage

Here is an example of how to use the library:

```python
from context_graph_builder import ContextGraphBuilder

# Initialize the graph builder
cg = ContextGraphBuilder()

# Add a decision node
cg.add_decision("decision_1", {"outcome": "positive"})

# Add an outcome node connected to the decision
cg.add_outcome("decision_1", "outcome_1", {"result": "success"})

# Query the graph
result = cg.query_graph("decision_1")
print(result)

# Visualize the graph
cg.visualize_graph()
```

## Testing

Run the tests using pytest:

```bash
pytest test_context_graph_builder.py
```

## License

This project is licensed under the MIT License.
