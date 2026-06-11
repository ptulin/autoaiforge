# AI Agent Task Orchestrator

## Overview
The AI Agent Task Orchestrator is a Python CLI tool that allows developers to create, customize, and orchestrate AI agents tailored to specific knowledge work tasks, such as summarization, code generation, or document analysis. It provides a modular architecture to define workflows where different AI models or APIs can be used to perform tasks in sequence.

## Features
- Load workflow configurations from YAML or JSON files.
- Execute workflows with multiple steps, each using a specified AI model and prompt.
- Save the results of the workflow execution to a specified output directory.

## Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ai_agent_task_orchestrator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool using the following command:

```bash
python ai_agent_task_orchestrator.py --config <path_to_config_file> --output <output_directory>
```

### Arguments
- `--config`: Path to the workflow configuration file (YAML or JSON format).
- `--input` (optional): Path to the input file for the AI agents.
- `--output`: Directory to save the results.

### Example
Create a YAML configuration file `workflow.yaml`:

```yaml
steps:
  - name: Summarize Text
    model: gpt-3.5-turbo
    prompt: "Summarize the following text: ..."
  - name: Generate Code
    model: gpt-3.5-turbo
    prompt: "Generate a Python function to calculate factorial."
```

Run the tool:

```bash
python ai_agent_task_orchestrator.py --config workflow.yaml --output ./results
```

## Testing
To run the tests, use `pytest`:

```bash
pytest test_ai_agent_task_orchestrator.py
```

The tests include:
- Validating the execution of a workflow defined in a YAML file.
- Handling of empty workflows.
- Handling of invalid configuration files.

## Requirements
- Python 3.7+
- `openai`
- `pyyaml`
- `pytest`

## License
This project is licensed under the MIT License.
