# LLM Router Middleware

## Description

`llm_router` is a Python CLI tool that dynamically routes requests to the most suitable large language model (LLM) based on the task type, such as summarization, translation, or text generation. It uses defined performance metrics like latency, accuracy, and cost to make optimized routing decisions.

## Features

- Load routing configurations from a YAML file.
- Select the most suitable LLM based on task type and priority.
- Send requests to the selected LLM and retrieve the response.
- Handle errors gracefully, including missing files, empty inputs, and network issues.

## Installation

Install the required Python packages using pip:

```bash
pip install pyyaml requests pytest
```

## Usage

Run the CLI tool with the following arguments:

```bash
python llm_router.py --task <task_type> --input_file <path_to_input_file> --config <path_to_config_file>
```

### Arguments

- `--task`: The task type (e.g., summarization, translation, text_generation).
- `--input_file`: Path to the input text file.
- `--config`: Path to the routing configuration file (YAML format).

### Example

```bash
python llm_router.py --task summarization --input_file input.txt --config config.yaml
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_router.py
```

The tests cover the following scenarios:

1. Loading a valid configuration file.
2. Selecting the most suitable LLM based on task type and priority.
3. Successfully calling an LLM endpoint.
4. Handling connection errors when calling an LLM endpoint.
5. Handling unsupported tasks.
6. Handling tasks with no configured LLMs.

## License

This project is licensed under the MIT License.