# Claude Agent Loop Runner

## Description
The Claude Agent Loop Runner is a CLI tool designed to simplify the creation and execution of agent loops using the Claude AI SDK. Users can define task workflows as JSON or YAML files, which the tool translates into Claude-compatible agent loops. This tool is ideal for developers looking to prototype complex multi-step AI workflows quickly.

## Features
- Load workflows from JSON or YAML files.
- Execute workflows using the Claude AI SDK.
- Set a maximum number of iterations for workflow execution.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python claude_agent_loop_runner.py --workflow <path_to_workflow_file> --max-iterations <max_iterations> --api-key <your_api_key>
```

### Arguments
- `--workflow`: Path to the workflow file (JSON or YAML).
- `--max-iterations`: Maximum number of iterations (default: 10).
- `--api-key`: Your Anthropic API key.

## Testing

Run the tests using pytest:

```bash
pytest test_claude_agent_loop_runner.py
```

## Requirements
- Python 3.7+
- anthropic
- pyyaml
- rich

## License
MIT License
