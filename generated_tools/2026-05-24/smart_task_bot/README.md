# Smart Task Automation Bot

Smart Task Automation Bot is a command-line tool that enables developers to define and execute reusable task sequences. These tasks can include API calls, AI agent interactions, and file input/output operations. The tool supports task sequence definitions via JSON files and provides configurable options for task execution.

## Features

- Define task sequences via JSON files or command-line arguments.
- Execute tasks such as API calls, AI agent interactions, and file I/O operations.
- Integrates with OpenAI for AI-powered tasks.
- Configurable retry policies and task-specific parameters.
- Save task results to files or output them to the console.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/smart-task-bot.git
   cd smart-task-bot
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Example Task JSON File

```json
[
    {
        "type": "api_call",
        "url": "https://api.example.com/data",
        "method": "GET"
    },
    {
        "type": "ai_agent",
        "api_key": "your_openai_api_key",
        "prompt": "Summarize this text",
        "model": "text-davinci-003",
        "max_tokens": 50
    },
    {
        "type": "file_io",
        "operation": "write",
        "file_path": "output.txt",
        "content": "Task completed successfully."
    }
]
```

### Run the Tool

```bash
python smart_task_bot.py --tasks tasks.json --output-dir ./results
```

### Output

- Results will be printed to the console.
- If `--output-dir` is specified, results will be saved to `results.json` in the specified directory.

## Testing

Run the tests using pytest:

```bash
pytest test_smart_task_bot.py
```

## License

This project is licensed under the MIT License.
