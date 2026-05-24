# AI Agent Flow

AI Agent Flow helps developers create, chain, and manage AI agent workflows involving tools like Claude, Gemini, or Codex. It allows seamless integration of multiple agents to automate complex tasks, such as data analysis, report generation, or multi-step decision-making processes, through a simple configuration file.

## Features

- Load workflows from YAML configuration files.
- Execute AI agents like OpenAI's ChatCompletion.
- Chain multiple agents to create complex workflows.
- Save workflow results to a file.

## Requirements

- Python 3.7+
- Required Python packages:
  - `openai`
  - `pyyaml`
  - `click`

Install the dependencies using pip:

```bash
pip install openai pyyaml click
```

## Usage

Run the tool using the command line:

```bash
python ai_agent_flow.py --config <path_to_config.yaml> --output <path_to_output.yaml>
```

### Arguments

- `--config`: Path to the YAML configuration file defining the workflow.
- `--output`: (Optional) Path to save the workflow results.

## Configuration File Format

The configuration file should be in YAML format and follow this structure:

```yaml
agents:
  agent1:
    type: openai
    model: gpt-3.5-turbo
workflow:
  - name: step1
    agent: agent1
    input: "Hello"
```

### Example

Save the following configuration to `example_workflow.yaml`:

```yaml
agents:
  agent1:
    type: openai
    model: gpt-3.5-turbo
workflow:
  - name: step1
    agent: agent1
    input: "Hello, how are you?"
```

Run the workflow:

```bash
python ai_agent_flow.py --config example_workflow.yaml --output results.yaml
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_agent_flow.py
```

## License

This project is licensed under the MIT License.