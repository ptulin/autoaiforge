# Claude Task Scheduler

This CLI tool enables developers to schedule and manage tasks within Claude AI's ecosystem. It leverages the task scheduling and unified memory features to create recurring or one-off AI-driven tasks, monitor their status, and retrieve results. This is useful for automating repetitive workflows.

## Features
- Schedule tasks with recurrence intervals.
- Send prompts to Claude AI.
- Save task results to a file.
- Load configuration from a YAML file.

## Installation

Install the required dependencies:

```bash
pip install httpx pyyaml pytest
```

## Usage

### Command Line Interface

```bash
python claude_task_scheduler.py --task-name "example_task" --interval "24h" --prompt "Example prompt" --api-url "https://api.claude.ai" --api-key "your_api_key"
```

### Using a Configuration File

Create a YAML configuration file (e.g., `config.yaml`):

```yaml
task_name: example_task
interval: 24h
prompt: Example prompt
output: output.json
```

Run the tool with the configuration file:

```bash
python claude_task_scheduler.py --config config.yaml --api-url "https://api.claude.ai" --api-key "your_api_key"
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_task_scheduler.py
```

All tests are self-contained and do not require network access.