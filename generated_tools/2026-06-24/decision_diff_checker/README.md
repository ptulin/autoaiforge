# Decision Diff Checker

## Overview
The Decision Diff Checker is a Python tool designed to help developers compare the decision-making paths of an AI agent across different versions or configurations. By highlighting differences in decisions, it enables developers to pinpoint where and why an agent's behavior diverges, making regression analysis and debugging more efficient.

## Features
- Compare two JSON files containing AI decision-making logs.
- Highlight differences in a human-readable format using the `rich` library.
- Handle edge cases such as missing files or invalid JSON formats.

## Installation
To use this tool, you need Python 3.7 or later. Install the required dependency using pip:

```bash
pip install rich
```

## Usage
Run the tool from the command line with the following arguments:

```bash
python decision_diff_checker.py --old_run <path_to_old_run.json> --new_run <path_to_new_run.json>
```

### Arguments
- `--old_run`: Path to the JSON file containing the old AI decision-making log.
- `--new_run`: Path to the JSON file containing the new AI decision-making log.

### Example
```bash
python decision_diff_checker.py --old_run old_run.json --new_run new_run.json
```

If there are differences between the two files, they will be displayed in a color-coded format:
- Lines added in the new file are shown in green.
- Lines removed from the old file are shown in red.

If there are no differences, the tool will display a message indicating that no differences were found.

## Testing
The tool includes a test suite written with `pytest`. To run the tests, install `pytest` and execute the following command:

```bash
pytest test_decision_diff_checker.py
```

The tests cover the following scenarios:
- Loading valid JSON files.
- Handling missing or invalid JSON files.
- Generating diffs between two JSON objects.
- Displaying diffs using the `rich` library.

## License
This project is licensed under the MIT License.
