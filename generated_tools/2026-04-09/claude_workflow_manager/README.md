# Claude Workflow Manager

## Overview

The Claude Workflow Manager is a Python tool that allows developers to define, chain, and execute complex Claude Managed Agent workflows via a simple YAML configuration. It streamlines the orchestration of multi-step AI tasks, such as data extraction, summarization, and decision-making, without requiring manual API calls.

## Features

- Load workflows from YAML files.
- Execute tasks sequentially or in parallel.
- Handle network errors and HTTP errors gracefully.
- Save results to a JSON file.

## Requirements

- Python 3.7+
- `httpx`
- `PyYAML`

Install the required dependencies using pip:

```bash
pip install httpx PyYAML
```

## Usage

Run the tool from the command line:

```bash
python claude_workflow_manager.py --workflow <path_to_workflow_yaml> --output <path_to_output_json>
```

### Example

Create a YAML file `workflow.yaml`:

```yaml
tasks:
  - name: task1
    endpoint: https://api.example.com/task1
    parameters:
      key: value1
    api_key: dummy_key1
  - name: task2
    endpoint: https://api.example.com/task2
    parameters:
      key: value2
    api_key: dummy_key2
execution_mode: sequential
```

Run the workflow:

```bash
python claude_workflow_manager.py --workflow workflow.yaml --output results.json
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_workflow_manager.py
```

The tests include:

- Loading a workflow from a YAML file.
- Executing a single task successfully.
- Handling task execution failures.
- Executing a workflow with multiple tasks sequentially.

All tests are self-contained and do not require network access.