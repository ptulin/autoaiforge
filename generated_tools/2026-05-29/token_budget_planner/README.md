# Token Budget Planner

## Overview
The Token Budget Planner is a CLI tool designed to help developers plan and visualize token budgets for multi-step LLM workflows. It calculates token usage for each step in a sequence of LLM calls and ensures the entire pipeline stays within token limits.

## Features
- Load and validate a JSON configuration file containing workflow steps.
- Estimate token usage for each step based on the prompt and model.
- Calculate token usage and check for token limit violations.
- Visualize token usage with a bar chart.

## Installation
To use this tool, you need Python installed on your system. Additionally, install the required dependencies:

```bash
pip install matplotlib
```

## Usage
Run the tool from the command line:

```bash
python token_budget_planner.py --config <path_to_config_file> [--output <output_image_path>]
```

- `--config`: Path to the JSON configuration file containing the workflow steps.
- `--output`: (Optional) Path to save the visualization image. If not provided, the chart will be displayed interactively.

## Configuration File Format
The configuration file should be a JSON file containing a list of steps. Each step should have the following fields:

- `name`: Name of the step.
- `prompt`: The prompt text for the LLM.
- `model`: The name of the LLM model.
- `max_tokens`: The maximum number of tokens allowed for this step.

Example:

```json
[
    {
        "name": "Step 1",
        "prompt": "Hello, how can I assist you today?",
        "model": "gpt-3.5-turbo",
        "max_tokens": 100
    },
    {
        "name": "Step 2",
        "prompt": "Please summarize the following text:",
        "model": "gpt-3.5-turbo",
        "max_tokens": 200
    }
]
```

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute the tests:

```bash
pytest test_token_budget_planner.py
```

## License
This project is licensed under the MIT License.