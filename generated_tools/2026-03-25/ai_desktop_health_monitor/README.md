# AI Desktop Health Monitor

## Overview
The AI Desktop Health Monitor is a Python tool that continuously monitors your desktop environment for performance bottlenecks, such as high CPU usage. It uses Claude AI to autonomously address these issues by suggesting actions like closing unresponsive applications or optimizing system resources.

## Features
- Monitors CPU usage in real-time.
- Configurable CPU usage threshold to trigger actions.
- Uses Claude AI to suggest actions when performance issues are detected.
- Handles invalid or missing configuration files gracefully.

## Requirements
- Python 3.7+
- `psutil` library

## Installation
Install the required Python package:
```bash
pip install psutil
```

## Usage
Run the script with the following arguments:

```bash
python ai_desktop_health_monitor.py --cpu-threshold <threshold> --claude-action-file <file_path> [--poll-interval <interval>]
```

### Arguments
- `--cpu-threshold`: CPU usage percentage threshold to trigger actions (required).
- `--claude-action-file`: Path to a JSON file containing Claude AI instructions (required).
- `--poll-interval`: Polling interval in seconds (default: 5).

### Example
```bash
python ai_desktop_health_monitor.py --cpu-threshold 80 --claude-action-file actions.json --poll-interval 10
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_ai_desktop_health_monitor.py
```

## Notes
- This tool uses a mock for the Claude AI client for testing purposes.
- Ensure the JSON file provided contains valid instructions for Claude AI.
