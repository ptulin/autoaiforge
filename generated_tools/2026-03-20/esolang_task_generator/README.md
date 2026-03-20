# Esoteric Task Generator

## Description
The Esoteric Task Generator is a Python library designed to generate tasks in esoteric programming languages, such as Brainfuck. This tool is useful for researchers and developers who want to create diverse and challenging benchmarks for evaluating language models (LLMs).

## Features
- Generate random programs in esoteric languages.
- Customizable templates for task generation.
- Validation utilities for syntactic correctness.

## Installation

Install the required dependencies:

```bash
pip install pyparsing==3.1.1 pytest==7.4.2
```

## Usage

### Import and Generate Tasks

```python
from esolang_task_generator import generate_task

# Generate a Brainfuck task with complexity 5
print(generate_task(language='brainfuck', complexity=5))
```

### Command-Line Interface

Run the script directly:

```bash
python esolang_task_generator.py --language brainfuck --complexity 10
```

## Example Output

```plaintext
Generated Task:
++[>++<-]
```

## Testing

Run the tests using pytest:

```bash
pytest test_esolang_task_generator.py
```

## Limitations
- Currently supports only Brainfuck as the esoteric language.
- Complexity must be a positive integer.

## License
This project is licensed under the MIT License.