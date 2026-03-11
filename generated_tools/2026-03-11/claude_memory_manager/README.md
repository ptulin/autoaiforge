# Claude Memory Manager

## Overview
The Claude Memory Manager is a Python tool designed to interact with Claude AI's memory feature. It allows developers to store, retrieve, and manage contextual information for better AI responses. This tool is particularly useful for maintaining long-term context across conversations or tasks.

## Features
- Save memory data to Claude AI using JSON or YAML files.
- Retrieve memory data from Claude AI.
- Delete specific memory entries from Claude AI.

## Requirements
- Python 3.7+
- `requests` library
- `pyyaml` library

Install the required libraries using:
```bash
pip install requests pyyaml
```

## Usage
Run the script with the following options:

### Save Memory
```bash
python claude_memory_manager.py --api-url <API_URL> --api-key <API_KEY> --save <FILE_PATH>
```
- `<API_URL>`: The base URL of the Claude AI API.
- `<API_KEY>`: Your Claude AI API key.
- `<FILE_PATH>`: Path to the JSON or YAML file containing memory data to save.

### Retrieve Memory
```bash
python claude_memory_manager.py --api-url <API_URL> --api-key <API_KEY> --retrieve [--output <OUTPUT_FILE>]
```
- `<OUTPUT_FILE>` (optional): Path to save the retrieved memory data as a JSON file.

### Delete Memory
```bash
python claude_memory_manager.py --api-url <API_URL> --api-key <API_KEY> --delete <MEMORY_ID>
```
- `<MEMORY_ID>`: The ID of the memory entry to delete.

## Testing
Run the tests using `pytest`:
```bash
pytest test_claude_memory_manager.py
```

All tests are self-contained and mock external network calls, ensuring they pass without network access.

## License
This project is licensed under the MIT License.