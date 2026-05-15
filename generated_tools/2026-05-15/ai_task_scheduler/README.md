# AI Task Scheduler

## Overview
The AI Task Scheduler is a Python tool that enables developers to schedule and automate business tasks powered by AI APIs. It allows users to configure periodic or event-driven tasks (e.g., generating reports, extracting key metrics) that leverage OpenAI's GPT models for smart processing, making it ideal for routine business automation.

## Features
- Load tasks from a YAML configuration file.
- Schedule tasks based on intervals or specific times.
- Execute tasks using OpenAI's GPT models.
- Save task outputs to specified files.

## Requirements
- Python 3.7+
- `openai`
- `pyyaml`
- `schedule`

## Installation
Install the required dependencies using pip:

```bash
pip install openai pyyaml schedule
```

## Usage
1. Create a YAML configuration file with the following structure:

```yaml
api_key: YOUR_OPENAI_API_KEY

tasks:
  task1:
    prompt: "Generate a report"
    output_file: "output.txt"
    schedule_type: "interval"
    interval: 10
```

2. Run the script with the path to your configuration file:

```bash
python ai_task_scheduler.py --config path/to/config.yaml
```

## Testing
Run the tests using `pytest`:

```bash
pytest test_ai_task_scheduler.py
```

## License
This project is licensed under the MIT License.