# Token Usage Visualizer

## Overview
The Token Usage Visualizer is a Python library and CLI tool designed to help developers analyze and visualize token usage data over time. It provides three types of charts: line charts, bar charts, and pie charts, allowing users to identify patterns, spikes, and optimization opportunities in AI application usage.

## Features
- Parse token usage data from CSV log files.
- Generate line charts, bar charts, and pie charts to visualize token usage.
- Save charts to files or display them interactively.

## Installation
To install the required dependencies, run:

```bash
pip install pandas matplotlib click
```

## Usage
You can use the tool via the command line or as a Python library.

### Command Line Interface

```bash
python token_usage_visualizer.py --log_file <path_to_csv> --chart_type <line|bar|pie> [--output <output_file>]
```

- `--log_file`: Path to the token usage log file (CSV format). The CSV file must contain `timestamp` and `tokens` columns.
- `--chart_type`: Type of chart to generate (`line`, `bar`, or `pie`).
- `--output`: (Optional) Path to save the chart image. If not provided, the chart will be displayed interactively.

### Example

```bash
python token_usage_visualizer.py --log_file data.csv --chart_type line --output chart.png
```

This command will generate a line chart of token usage over time from the `data.csv` file and save it as `chart.png`.

### Library Usage

You can also use the tool as a Python library:

```python
import pandas as pd
from token_usage_visualizer import parse_log_file, generate_line_chart

# Parse the log file
data = parse_log_file("data.csv")

# Generate a line chart
generate_line_chart(data, output_file="chart.png")
```

## Testing
To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run:

```bash
pytest test_token_usage_visualizer.py
```

All tests should pass successfully.

## License
This project is licensed under the MIT License.