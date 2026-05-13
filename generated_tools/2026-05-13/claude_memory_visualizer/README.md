# Claude Memory Visualizer

## Overview
The Claude Memory Visualizer is a command-line tool that fetches and visualizes memory data from an API. It allows developers to filter, display, and export memory entries in a human-readable format. This tool is useful for debugging and understanding the memory usage of AI applications.

## Features
- Fetch memory data from a specified API endpoint.
- Filter memory entries by keyword or timestamp.
- Display memory entries in a tabular format.
- Export memory data to JSON or CSV files.

## Installation
Install the required dependencies using pip:

```bash
pip install tabulate requests
```

## Usage
Run the tool from the command line:

```bash
python claude_memory_visualizer.py --api-url <API_URL> [--filter <KEYWORD>] [--since <YYYY-MM-DD>] [--output <json/csv>] [--output-file <FILE_PATH>]
```

### Arguments
- `--api-url`: The API URL to fetch memory data (required).
- `--filter`: A keyword to filter memory entries (optional).
- `--since`: Filter entries since a specific timestamp in `YYYY-MM-DD` format (optional).
- `--output`: The output format for exporting data (`json` or `csv`) (optional).
- `--output-file`: The file path to save exported data (required if `--output` is specified).

### Examples

#### Display memory data in a table
```bash
python claude_memory_visualizer.py --api-url http://mockapi.com/memory
```

#### Filter memory data by keyword and display
```bash
python claude_memory_visualizer.py --api-url http://mockapi.com/memory --filter "Test"
```

#### Filter memory data by date and export to JSON
```bash
python claude_memory_visualizer.py --api-url http://mockapi.com/memory --since 2023-10-01 --output json --output-file memory.json
```

## Testing
Run the tests using pytest:

```bash
pytest test_claude_memory_visualizer.py
```

## License
This project is licensed under the MIT License.