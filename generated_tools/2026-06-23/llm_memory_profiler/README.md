# LLM Memory Profiler

## Overview

The **LLM Memory Profiler** is a Python tool designed to profile the memory usage of locally hosted large language models during inference. It provides detailed breakdowns of memory allocation, identifies bottlenecks, and offers actionable recommendations to optimize memory usage for constrained environments.

## Features

- Profiles memory usage of Python scripts using large language models.
- Provides a breakdown of memory allocations by file and line number.
- Identifies potential memory bottlenecks and suggests optimization strategies.

## Installation

Install the required dependency using pip:

```bash
pip install psutil
```

## Usage

Run the profiler on a Python script using the following command:

```bash
python llm_memory_profiler.py --script <path_to_script>
```

### Example

```bash
python llm_memory_profiler.py --script my_model_script.py
```

## Output

The tool will output:

- Initial memory usage (in MB).
- Peak memory usage (in MB).
- A breakdown of memory usage by file and line number.
- Optimization tips if high memory usage or large allocations are detected.

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_memory_profiler.py
```

## License

This project is licensed under the MIT License.