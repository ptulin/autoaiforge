# Skill Registry Builder

This library helps developers build and manage skill-based command systems for Claude AI. It provides a framework for defining, testing, and registering skills as modular Python functions, making it easy to scale and maintain a skill set for complex use cases.

## Features

- Register skills with metadata (name, description, inputs, outputs).
- Validate skill inputs.
- Execute registered skills with validated inputs.
- Generate a JSON registry of all registered skills.
- Generate documentation for all registered skills.

## Installation

Install the required dependencies using pip:

```bash
pip install pydantic typer
```

## Usage

### Registering a Skill

```python
from skill_registry_builder import register_skill

def greet(name: str) -> str:
    return f"Hello, {name}!"

metadata = {
    "name": "greet",
    "description": "Greets a user by name.",
    "inputs": {"name": "str"},
    "outputs": {"greeting": "str"}
}

register_skill(greet, metadata)
```

### Generating Registry JSON

```bash
python skill_registry_builder.py generate-registry --output-file registry.json
```

### Generating Documentation

```bash
python skill_registry_builder.py generate-docs --output-file docs.md
```

## Testing

Run the tests using pytest:

```bash
pytest test_skill_registry_builder.py
```

Ensure all tests pass successfully.