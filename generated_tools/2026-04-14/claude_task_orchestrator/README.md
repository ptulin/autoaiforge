# Claude Task Orchestrator

## Description
The Claude Task Orchestrator is a Python-based automation tool that allows users to chain multiple Claude AI tasks into a seamless workflow. It is designed for small businesses and developers to automate repetitive tasks such as document editing, email composition, and file organization. The tool supports JSON-based workflow definitions and provides CLI configuration for ease of use.

## Features
- Chain multiple Claude AI tasks into a single workflow.
- Built-in presets for common business tasks like email drafting and file sorting.
- Supports CLI configuration and JSON-based workflow definitions.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/claude_task_orchestrator.git
   cd claude_task_orchestrator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-Line Interface

Run the tool using the following command:

```bash
python claude_task_orchestrator.py --workflow config.json --input data/input_folder/ --api_key YOUR_API_KEY
```

- `--workflow`: Path to the JSON file defining the workflow.
- `--input`: Path to the input data (e.g., a text file or folder).
- `--api_key`: Your Claude API key.

### Example Workflow Configuration

```json
{
    "tasks": [
        {
            "name": "Draft Email",
            "prompt_template": "Draft a professional email based on the following input: {input}",
            "max_tokens": 150
        },
        {
            "name": "Summarize Document",
            "prompt_template": "Summarize the following text: {input}",
            "max_tokens": 100
        }
    ]
}
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_task_orchestrator.py
```

## License
This project is licensed under the MIT License.
