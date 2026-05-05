# Agent Task Orchestrator

## Overview
The Agent Task Orchestrator is a Python tool that allows developers to create and manage autonomous AI agents capable of executing multi-step workflows. It provides a framework for defining tasks, dependencies, and execution logic, making it easier to build robust and reusable agent-driven workflows.

## Features
- Define workflows using YAML or JSON configuration files.
- Validate configurations against a predefined schema.
- Execute tasks with dependency management.
- Save execution results to a file or display them in the console.

## Installation

Install the required dependencies:

```bash
pip install typer rich jsonschema pyyaml
```

## Usage

Run the tool using the following command:

```bash
python agent_task_orchestrator.py --config <path_to_config_file> [--output <path_to_output_file>]
```

### Arguments
- `--config`: Path to the YAML or JSON configuration file defining the workflow.
- `--output` (optional): Path to save the execution results in JSON format.

## Configuration File Format

The configuration file must be in YAML or JSON format and adhere to the following schema:

```yaml
tasks:
  - id: "task1"
    description: "Description of task 1"
    action: "action1"
    dependencies: []
  - id: "task2"
    description: "Description of task 2"
    action: "action2"
    dependencies: ["task1"]
```

## Testing

Run the tests using pytest:

```bash
pytest test_agent_task_orchestrator.py
```

The tests include:
- Validation of correct configuration files.
- Detection of invalid configuration files.
- Execution of workflows with dependencies.

## License

This project is licensed under the MIT License.
