# Claude Memory Manager

## Description
Claude Memory Manager is a Python tool that allows developers to interact with Claude AI's self-updating memory feature. It enables querying, adding/updating, and deleting memory entries programmatically, providing fine-grained control over AI-driven workflows.

## Installation

1. Clone the repository or download the script.
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the tool with the appropriate CLI arguments:

### Query Memory
```bash
python claude_memory_manager.py --api-url http://api.example.com --query project_status
```

### Add or Update Memory
```bash
python claude_memory_manager.py --api-url http://api.example.com --add project_status completed
```

### Delete Memory
```bash
python claude_memory_manager.py --api-url http://api.example.com --delete project_status
```

## Features

- **Query Memory**: Retrieve memory entries by key.
- **Add/Update Memory**: Add new memory entries or update existing ones.
- **Delete Memory**: Remove outdated or irrelevant memory entries.

## Testing

Run the tests using `pytest`:

```bash
pytest test_claude_memory_manager.py
```

All external API calls are mocked to ensure tests pass without network access.

## License

MIT License