# Smart Task Scheduler

## Overview

The Smart Task Scheduler is a Python-based CLI tool that allows developers to schedule and execute tasks using a configuration file. Tasks can include API requests, custom scripts, or other operations, and they can be triggered based on time (cron-like scheduling).

## Features

- Load tasks from a JSON or YAML configuration file.
- Schedule tasks using cron-like time triggers.
- Execute tasks such as API requests or custom Python scripts.
- Log task execution details to a rotating log file.

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool with the following command:

```bash
python smart_task_scheduler.py --config /path/to/config.json
```

### Configuration File Format

The configuration file should be in JSON or YAML format and include a list of tasks. Each task should have the following structure:

```json
{
  "tasks": [
    {
      "name": "Task Name",
      "type": "api_request",
      "method": "GET",
      "url": "https://example.com/api",
      "trigger": {"cron": "12:00"}
    },
    {
      "name": "Another Task",
      "type": "custom_script",
      "script": "print('Hello, World!')",
      "trigger": {"cron": "13:00"}
    }
  ]
}
```

## Testing

Run the tests using pytest:

```bash
pytest test_smart_task_scheduler.py
```

## License

MIT License
