# Claude Memory Importer

## Overview
Claude Memory Importer is a Python utility designed to batch-upload custom datasets or memory snippets into Claude AI for personalized interactions. This tool helps developers pre-load domain-specific knowledge or project context to tailor Claude's responses to their exact needs.

## Features
- Supports JSON and CSV input formats.
- Validates and sanitizes input data.
- Handles errors gracefully during data upload.
- Provides detailed upload results for each memory snippet.

## Installation

Install the required Python package:

```bash
pip install pandas
```

## Usage

Run the script using the command line:

```bash
python claude_memory_importer.py --file <path_to_file> --api-key <your_api_key>
```

### Arguments
- `--file`: Path to the input JSON or CSV file containing memory snippets.
- `--api-key`: Your Claude API key.

### Example

```bash
python claude_memory_importer.py --file snippets.json --api-key your_api_key
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_claude_memory_importer.py
```

## License
MIT License
