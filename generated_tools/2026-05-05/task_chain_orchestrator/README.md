# Task Chain Orchestrator

## Overview
The Task Chain Orchestrator is a Python-based tool that allows developers to define, run, and automate complex task chains using AI assistants. Users can specify sequential or conditional tasks, and the AI dynamically reacts to intermediate outputs to decide the next step. This tool is useful for automating workflows that involve multiple steps.

## Features
- Define sequential and conditional tasks in a JSON configuration file.
- Dynamically execute tasks based on AI responses and conditions.
- Log task execution and results for easy debugging.

## Requirements
- Python 3.7+
- `requests` library
- `pytest` for testing

## Installation
1. Clone the repository.
2. Install the required dependencies:
   ```bash
   pip install requests pytest
   ```

## Usage
Run the tool using the following command:
```bash
python task_chain_orchestrator.py --config <path_to_config_file> --api_url <api_url> --api_key <api_key>
```

### Arguments
- `--config`: Path to the JSON configuration file containing the task chain.
- `--api_url`: The API endpoint URL for the AI model.
- `--api_key`: The API key for the AI model.

### Configuration File Format
The configuration file should be a JSON file with the following structure:
```json
{
  "tasks": [
    {
      "type": "sequential",
      "prompt": "Your first task prompt here"
    },
    {
      "type": "conditional",
      "prompt": "Your conditional task prompt here",
      "condition": "len(results) > 0"
    }
  ]
}
```
- `type`: The type of the task (`sequential` or `conditional`).
- `prompt`: The input prompt for the AI model.
- `condition`: (Optional) A Python expression to evaluate whether the task should be executed. The `results` variable contains the results of previous tasks.

## Testing
Run the tests using pytest:
```bash
pytest test_task_chain_orchestrator.py
```

The test suite includes:
1. Testing successful API calls.
2. Testing API call failures.
3. Testing task chain execution with mocked API responses.

## License
This project is licensed under the MIT License.