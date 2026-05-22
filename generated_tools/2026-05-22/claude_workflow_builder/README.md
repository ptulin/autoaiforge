# Claude Workflow Builder

## Overview

Claude Workflow Builder is a Python tool that allows developers to define and execute complex business workflows using Claude AI. By providing a YAML or JSON workflow file with tasks, decisions, and AI prompts, the tool orchestrates calling Claude AI and automates multi-step business processes.

## Features

- Load and validate workflow files in YAML or JSON format.
- Execute workflows step-by-step.
- Integrate with Claude AI for task and decision execution.

## Installation

Install the required dependencies:

```bash
pip install jsonschema openai pyyaml
```

## Usage

Run the tool with the path to a workflow file:

```bash
python claude_workflow_builder.py --workflow path/to/workflow.yaml
```

## Workflow File Format

The workflow file should be in YAML or JSON format and follow this schema:

```yaml
steps:
  - name: Step 1
    type: task
    prompt: "What is the capital of France?"
  - name: Step 2
    type: decision
    prompt: "Should we proceed?"
    options:
      max_tokens: 50
      temperature: 0.5
```

## Testing

Run tests using pytest:

```bash
pytest test_claude_workflow_builder.py
```

## License

This project is licensed under the MIT License.