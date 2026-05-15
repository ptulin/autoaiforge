# Claude Batch Automator

## Overview
Claude Batch Automator is a Python tool for batch-processing datasets using Claude AI Skills. It allows developers to efficiently run automation tasks, such as summarization or classification, on large datasets.

## Features
- Supports CSV, JSON, and TXT input file formats.
- Applies Claude AI skills to process data.
- Outputs processed data in the same format as the input file.
- Handles network errors gracefully.

## Installation
To use this tool, install the required dependencies:

```bash
pip install requests pandas tqdm
```

## Usage
Run the tool from the command line:

```bash
python claude_batch_automator.py --input <input_file> --skill <skill_name> --output <output_file>
```

### Arguments
- `--input`: Path to the input file (CSV, JSON, or TXT).
- `--skill`: Claude AI skill to apply (e.g., 'summarize').
- `--output`: Path to the output file.

### Example
```bash
python claude_batch_automator.py --input data.csv --skill summarize --output output.csv
```

## Testing
To run tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_claude_batch_automator.py
```

## License
This project is licensed under the MIT License.