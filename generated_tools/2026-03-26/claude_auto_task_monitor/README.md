# Claude Auto Task Monitor

## Description
Claude Auto Task Monitor is a Python library and CLI tool that tracks and visualizes the execution of Claude AI's Auto-Mode tasks in real time. It provides insights into task progress, success rates, and performance metrics via a local web dashboard. This tool is ideal for developers who want better visibility into AI-driven task automation.

## Features
- Real-time monitoring of Claude AI tasks.
- Local web dashboard for task status and metrics.
- Configurable alerts for task failures or delays.

## Installation

Install the required dependencies:

```bash
pip install flask==2.3.2 rich==13.4.1
```

## Usage

Run the tool with a JSON file containing task details:

```bash
python claude_auto_task_monitor.py --input tasks.json
```

## Example JSON Input

```json
[
  {
    "id": "1",
    "progress": 0
  },
  {
    "id": "2",
    "progress": 0
  }
]
```

## Development

Run tests using pytest:

```bash
pytest test_claude_auto_task_monitor.py
```

## License
MIT