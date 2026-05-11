# Long-Term Memory Inspector

## Description
The Long-Term Memory Inspector is a Python library designed to help AI developers monitor and manage long-term memory in AI systems. It provides utilities to query, filter, and prune memory storage programmatically. Additionally, the library can summarize memory contents for quick inspection, ensuring that the AI's memory remains relevant and efficient over time.

## Features
- **Query Memory**: Search for specific keywords within memory entries.
- **Prune Memory**: Remove outdated or irrelevant memory entries based on custom conditions.
- **Summarize Memory**: Generate a concise summary of memory contents for quick inspection.

## Installation
To install the required dependencies, run:
```bash
pip install pandas==1.5.3 numpy==1.23.5
```

## Usage Example
```python
from long_term_memory_inspector import MemoryInspector

# Example memory data
memory_data = [
    "Learned about pandas library.",
    "Attended a meeting on AI ethics.",
    "Read a paper on reinforcement learning.",
    "Discussed project goals with the team."
]

# Initialize the MemoryInspector
inspector = MemoryInspector(memory_data)

# Query memory
query_result = inspector.query("pandas")
print("Query Result:", query_result)

# Prune memory
pruned_memory = inspector.prune(lambda x: "pandas" in x)
print("Pruned Memory:", pruned_memory)

# Summarize memory
summary = inspector.summarize(width=50)
print("Memory Summary:", summary)
```

## Command-Line Interface
You can also use the library from the command line:

```bash
python long_term_memory_inspector.py --query "pandas" --summarize --width 50
```

## License
This project is licensed under the MIT License.
