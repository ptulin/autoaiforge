# Claude Change Tracker

## Overview

The Claude Change Tracker is a Python tool designed to track and highlight changes in Claude's performance metrics over time. By comparing two datasets containing input-output pairs and expected results, this tool helps developers assess the impact of Claude's learning iterations on task-specific performance.

## Features

- Compare two datasets with input-output pairs and expected results.
- Calculate metrics such as improvement, worsening, and unchanged rates.
- Generate a detailed summary and save it as a CSV file.

## Installation

Install the required dependencies using pip:

```bash
pip install pandas numpy
```

## Usage

Run the tool from the command line:

```bash
python claude_change_tracker.py <dataset_v1.csv> <dataset_v2.csv> <output.csv>
```

- `<dataset_v1.csv>`: Path to the first dataset (CSV format).
- `<dataset_v2.csv>`: Path to the second dataset (CSV format).
- `<output.csv>`: Path to save the output summary (CSV format).

## Example

```bash
python claude_change_tracker.py dataset_v1.csv dataset_v2.csv output.csv
```

## Testing

To run the tests, install `pytest` and execute the test file:

```bash
pip install pytest
pytest test_claude_change_tracker.py
```

## License

This project is licensed under the MIT License.