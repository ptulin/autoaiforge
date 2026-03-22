# Workflow Agent Builder

## Description
Workflow Agent Builder is a Python library for creating AI-powered workflow automation agents using YAML-based task definitions. This tool allows developers to define workflows with natural language prompts and actions, which are interpreted and executed by AI agents.

## Features
- **YAML-based declarative workflow definitions**
- **Pluggable AI models** (e.g., OpenAI)
- **Support for conditional task branching and loops**

## Installation
Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage
To execute a workflow:
```bash
python workflow_agent_builder.py --workflow tasks.yaml --api-key YOUR_API_KEY
```

Optionally, you can save the output to a JSON file:
```bash
python workflow_agent_builder.py --workflow tasks.yaml --api-key YOUR_API_KEY --output results.json
```

### Example YAML Workflow
```yaml
tasks:
  - name: "Task 1"
    prompt: "What is 2+2?"
    max_tokens: 10
  - name: "Conditional Task"
    prompt: "What is the capital of France?"
    condition: "Is this a test?"
    max_tokens: 10
```

## Testing
Run the tests using pytest:
```bash
pytest test_workflow_agent_builder.py
```

## License
MIT License