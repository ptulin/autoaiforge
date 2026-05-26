# Claude Memory Manager

Claude Memory Manager is a Python CLI and library tool designed to help developers optimize memory usage for Anthropic's Claude AI. The tool enables developers to segment prompts and responses, track memory utilization, and simulate clearing memory when limits are reached.

## Features
- Monitor system memory usage.
- Segment large prompts into smaller chunks for efficient processing.
- Simulate clearing memory.
- Interact with Claude AI using memory-efficient chunks.

## Installation

Install the required dependencies using pip:

```bash
pip install psutil tqdm
```

## Usage

Run the tool from the command line:

```bash
python claude_memory_manager.py --prompt "Your prompt here" --max-chunk-size 2000
```

### Options
- `--monitor-memory`: Monitor memory usage.
- `--max-memory`: Set the maximum memory limit in MB (default: 8000).
- `--clear-memory`: Simulate clearing memory.
- `--prompt`: Specify the prompt to send to Claude AI.
- `--max-chunk-size`: Set the maximum chunk size in bytes (default: 2000).

## Testing

Run tests using pytest:

```bash
pytest test_claude_memory_manager.py
```

## License

This project is licensed under the MIT License.