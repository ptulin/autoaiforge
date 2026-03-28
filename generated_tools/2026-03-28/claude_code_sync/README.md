# Claude Code Sync

## Description
`claude_code_sync` is a Python-based CLI tool that enables developers to sync local code files with Claude AI's real-time collaboration feature. It allows seamless two-way syncing between a local development environment and Claude, enabling developers to collaborate on code updates efficiently.

## Features
- Real-time synchronization of local files with Claude AI.
- Two-way syncing: Updates from Claude AI are reflected in local files and vice versa.
- Handles network errors gracefully.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd claude_code_sync
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python claude_code_sync.py --dir <directory_path> --api-key <your_claude_api_key>
```

- `--dir`: Path to the local directory to sync.
- `--api-key`: Your Claude API key.

Example:

```bash
python claude_code_sync.py --dir ./my_project --api-key abc123
```

## Testing

To run the tests, install `pytest` and execute:

```bash
pytest test_claude_code_sync.py
```

The tests include:
- Successful file synchronization.
- Handling cases where no changes are detected.
- Graceful handling of network errors.

## Requirements
- Python 3.7+
- `watchdog`
- `requests`
- `pytest`

## License
MIT License
