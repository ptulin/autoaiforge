# Recursive Prompt Optimizer

This Python library provides utilities to design and optimize prompts for recursive reasoning models. It includes tools to simulate recursive chains, measure token efficiency, and automatically refine prompts to minimize token usage without compromising reasoning quality.

## Features

- **Simulate Recursive Chains**: Simulate recursive reasoning chains using a prompt template and task configuration.
- **Measure Token Efficiency**: Calculate the number of tokens used by a given prompt.
- **Optimize Prompts**: Automatically refine prompts to reduce token usage while maintaining reasoning quality.

## Installation

Install the required dependencies using pip:

```bash
pip install nltk openai tiktoken
```

## Usage

### Command Line Interface

Run the script from the command line:

```bash
python recursive_prompt_optimizer.py "<prompt_template>" "<task_config_json>" --max_depth <max_depth> --max_iterations <max_iterations>
```

- `prompt_template`: The prompt template to optimize.
- `task_config_json`: JSON string of task configuration.
- `--max_depth`: Maximum recursion depth for simulation (default: 3).
- `--max_iterations`: Maximum iterations for optimization (default: 5).

### Example

```bash
python recursive_prompt_optimizer.py "What is the result of {input}?" "{\"input\": \"2 + 2\"}" --max_depth 2 --max_iterations 3
```

### Programmatic Usage

Import the library and use its functions in your Python code:

```python
from recursive_prompt_optimizer import simulate_recursive_chain, measure_token_efficiency, optimize_prompt

prompt_template = "What is the result of {input}?"
task_config = {"input": "2 + 2"}

# Simulate recursive chain
simulation_results = simulate_recursive_chain(prompt_template, task_config, max_depth=2)
print(simulation_results)

# Optimize prompt
optimization_results = optimize_prompt(prompt_template, task_config, max_iterations=5)
print(optimization_results)
```

## Testing

Run the tests using pytest:

```bash
pytest test_recursive_prompt_optimizer.py
```

## License

This project is licensed under the MIT License.