# AI Task Flow

## Overview
AI Task Flow is a Python tool that allows developers to define, manage, and execute automated workflows powered by AI models like OpenAI's GPT. It simplifies chaining multiple tasks, handling dependencies, and leveraging AI models for decision-making and data transformation.

## Features
- Define workflows in YAML or JSON format.
- Execute tasks sequentially based on dependencies.
- Use AI models for decision-making or data transformation.

## Installation
Install the required Python packages:

```bash
pip install openai pyyaml networkx
```

## Usage
Run the tool from the command line:

```bash
python ai_task_flow.py --workflow <path_to_workflow_file> --api-key <your_openai_api_key>
```

### Workflow File Format
The workflow file can be in YAML or JSON format. Example:

#### YAML:
```yaml
tasks:
  - name: task1
    dependencies: []
    ai_step:
      prompt: "What is the weather today?"
  - name: task2
    dependencies: [task1]
    ai_step:
      prompt: "What is the temperature today?"
```

#### JSON:
```json
{
  "tasks": [
    {
      "name": "task1",
      "dependencies": [],
      "ai_step": {
        "prompt": "What is the weather today?"
      }
    },
    {
      "name": "task2",
      "dependencies": ["task1"],
      "ai_step": {
        "prompt": "What is the temperature today?"
      }
    }
  ]
}
```

## Testing
Run the tests using pytest:

```bash
pytest test_ai_task_flow.py
```

## License
MIT License