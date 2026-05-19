# Workflow Auto-Generator

## Description
Workflow Auto-Generator is a Python-based automation tool that generates CI/CD or coding task automation workflows (e.g., GitHub Actions YAML files) based on natural language prompts. It simplifies the creation of complex automation workflows by leveraging AI.

## Features
- AI-powered generation of CI/CD workflows from natural language descriptions.
- Supports multiple workflow providers like GitHub Actions and GitLab CI.
- Validates generated YAML files for syntax correctness.

## Installation

1. Clone this repository or download the `workflow_autogenerator.py` file.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool using the following command:

```bash
python workflow_autogenerator.py --prompt "Build and test a Python package on push events" --platform github --output workflow.yml --api-key YOUR_OPENAI_API_KEY
```

### Arguments
- `--prompt`: Natural language description of the desired workflow.
- `--platform`: Target platform for the workflow (e.g., `github` or `gitlab`).
- `--output`: Output file to save the generated workflow YAML.
- `--api-key`: OpenAI API key.

## Example

```bash
python workflow_autogenerator.py --prompt "Deploy a Node.js application to production on push to main branch" --platform github --output deploy.yml --api-key YOUR_OPENAI_API_KEY
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_workflow_autogenerator.py
```

## License
This project is licensed under the MIT License.