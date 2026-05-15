# Claude Usage Monitor

`claude_usage_monitor` is a Python library and CLI tool to track usage of Claude AI's API in real-time. It helps developers monitor their API usage, optimize performance, and avoid exceeding usage limits.

## Features

- Fetch real-time usage data from the Claude API.
- Monitor API usage in real-time and receive alerts when usage exceeds a specified threshold.
- Generate usage reports over a specified time range, including CSV and graphical output.

## Installation

Install the required dependencies using pip:

```bash
pip install requests pandas matplotlib
```

## Usage

### CLI

#### Monitor Usage

Run the tool in monitoring mode to track usage in real-time:

```bash
python claude_usage_monitor.py --api-key YOUR_API_KEY --alert-threshold 80
```

- `--api-key`: Your Claude API key (required).
- `--alert-threshold`: Alert threshold percentage (default: 80).

#### Generate Report

Generate a usage report for the last N minutes:

```bash
python claude_usage_monitor.py --api-key YOUR_API_KEY --generate-report --time-range 60 --output-file usage_report.csv
```

- `--api-key`: Your Claude API key (required).
- `--generate-report`: Flag to generate a usage report.
- `--time-range`: Time range for the report in minutes (default: 60).
- `--output-file`: Output file for the report (default: `usage_report.csv`).

### Library

You can also use the functions programmatically:

```python
from claude_usage_monitor import fetch_usage, monitor_usage, generate_report

# Fetch usage data
usage_data = fetch_usage("YOUR_API_KEY")

# Monitor usage
monitor_usage("YOUR_API_KEY", alert_threshold=80)

# Generate a report
generate_report("YOUR_API_KEY", time_range=60, output_file="usage_report.csv")
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_claude_usage_monitor.py
```

The tests use mocking to simulate API responses and avoid making real network calls.

## License

This project is licensed under the MIT License.
