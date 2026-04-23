# AI Task Validator

## Overview
The AI Task Validator is a Python tool for validating task definitions and logic for autonomous AI agents. It ensures that tasks are correctly defined, dependencies are resolvable, and logic does not lead to deadlocks or circular dependencies. Additionally, it provides optimization suggestions to improve task efficiency.

## Features
- Validates task definitions for correctness.
- Detects circular dependencies.
- Identifies missing dependencies.
- Suggests optimizations to reduce redundancy in task outputs.

## Installation
Install the required dependencies using pip:

```bash
pip install pydantic networkx
```

## Usage

### Command Line Interface

Run the tool from the command line by providing an input JSON file with task definitions and an output file to save the validation report:

```bash
python ai_task_validator.py <input_file> <output_file>
```

### Example

Input JSON file (`tasks.json`):

```json
[
    {"id": "task1", "dependencies": [], "inputs": ["input1"], "outputs": ["output1"]},
    {"id": "task2", "dependencies": ["task1"], "inputs": ["output1"], "outputs": ["output2"]}
]
```

Run the tool:

```bash
python ai_task_validator.py tasks.json report.json
```

Output JSON file (`report.json`):

```json
{
    "status": "success",
    "message": "Tasks validated successfully.",
    "optimizations": []
}
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_task_validator.py
```

## License
MIT License