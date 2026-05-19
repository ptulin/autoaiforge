# Recursive Token Profiler

## Description
The Recursive Token Profiler is a Python-based CLI tool designed to evaluate and profile the token usage of recursive AI models. By simulating recursive reasoning tasks, this tool helps developers identify bottlenecks in token usage and optimize models for tasks involving large token contexts. It is particularly useful for experimenting with Stanford-style recursive AI models.

## Features
- Profiles token usage for recursive reasoning tasks.
- Simulates recursive calls and measures token growth.
- Outputs insightful metrics for model optimization.
- Generates visualizations of token growth across recursive depths.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd recursive_token_profiler
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Interface

```bash
python recursive_token_profiler.py --config task_config.json --output token_report.json --visual token_growth.png
```

- `--config`: Path to the JSON configuration file specifying the recursive task parameters and model type.
- `--output`: Path to save the token usage report as a JSON file.
- `--visual` (optional): Path to save the token growth visualization as an image.

### Example Configuration File

```json
{
  "model": "gpt-3.5-turbo",
  "task": "Simulate recursive reasoning task.",
  "max_depth": 5,
  "token_limit": 4096
}
```

### Example Output

A sample token usage report:

```json
{
  "depth": 1,
  "tokens": 123,
  "child": {
    "depth": 2,
    "tokens": 246,
    "child": {
      "depth": 3,
      "tokens": 369
    }
  }
}
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_recursive_token_profiler.py
```

## License
This project is licensed under the MIT License.
