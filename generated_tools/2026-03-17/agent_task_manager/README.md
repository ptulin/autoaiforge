# Agent Task Manager

## Overview

`agent_task_manager` is a Python library to manage and orchestrate autonomous agents performing collaborative tasks. It provides APIs to define agents, assign tasks, and monitor execution with support for dependency resolution and prioritization. This tool is useful for developers working on distributed AI systems and task planning workflows.

## Features

- Define tasks with dependencies and priorities.
- Assign tasks to agents.
- Execute tasks in order of priority and resolve dependencies.
- Asynchronous task execution using Celery.

## Installation

Install the required dependencies using pip:

```bash
pip install pydantic celery redis
```

## Usage

### Example

```python
from agent_task_manager import AgentTaskManager

manager = AgentTaskManager()
manager.add_task(agent_id=1, task_name="fetch_data")
manager.add_task(agent_id=1, task_name="process_data", dependencies=["fetch_data"])
manager.execute_tasks()
```

### Running Celery Worker

Ensure you have a Redis server running locally. Start a Celery worker with the following command:

```bash
celery -A agent_task_manager worker --loglevel=info
```

## Testing

Run the tests using pytest:

```bash
pytest test_agent_task_manager.py
```

## License

This project is licensed under the MIT License.