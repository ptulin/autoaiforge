# Claude Task Dispatcher

## Overview

`claude_task_dispatcher` is a CLI tool that integrates with Claude AI's dispatch features to schedule and manage tasks programmatically. This tool enables developers to define workflows and automatically execute them based on predefined triggers or schedules, enhancing productivity in AI-related projects.

## Features

- Load workflows from JSON or YAML files.
- Execute tasks defined in workflows.
- Schedule workflows using cron-like expressions.

## Installation

Install the required dependencies using pip:

```bash
pip install requests schedule pyyaml
```

## Usage

Run the tool using the command line:

```bash
python claude_task_dispatcher.py --workflow <path_to_workflow_file> [--execute | --schedule <cron_expression>]
```

### Options

- `--workflow`: Path to the workflow file (JSON or YAML).
- `--execute`: Immediately execute the workflow.
- `--schedule`: Schedule the workflow using a cron-like expression (e.g., `*/15 * * * *`).

### Example

To execute a workflow immediately:

```bash
python claude_task_dispatcher.py --workflow example_workflow.json --execute
```

To schedule a workflow:

```bash
python claude_task_dispatcher.py --workflow example_workflow.yaml --schedule "*/15 * * * *"
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_task_dispatcher.py
```

## License

This project is licensed under the MIT License.