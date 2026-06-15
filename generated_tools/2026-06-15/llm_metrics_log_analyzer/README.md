# LLM Metrics Log Analyzer

## Description
The **LLM Metrics Log Analyzer** is a Python CLI tool designed to parse logs generated during LLM (Large Language Model) inference. It extracts and aggregates performance metrics such as average latency, token usage distribution, and error counts. The results can be output in JSON, CSV, or console format, making it suitable for both real-time monitoring and offline analysis.

## Features
- Parses logs and extracts LLM performance metrics.
- Supports customizable log formats using regular expressions.
- Generates visualizable output in JSON, CSV, or console summaries.
- Ideal for post-hoc performance debugging and monitoring.

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd llm_metrics_log_analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Usage

```bash
python llm_metrics_log_analyzer.py --log-file inference.log --log-format "<regex-pattern>" --output-format csv --output-file metrics.csv
```

### Arguments
- `--log-file`: Path to the log file to analyze.
- `--log-format`: Regex pattern to parse the log entries.
- `--output-format`: Output format (`json`, `csv`, or `console`). Default is `console`.
- `--output-file`: Path to save the output file (required for `json` or `csv` output).

### Example

```bash
python llm_metrics_log_analyzer.py \
    --log-file inference.log \
    --log-format "(?P<timestamp>.*) latency=(?P<latency>\d+) tokens=(?P<tokens>\d+) status=(?P<status>\w+)" \
    --output-format json \
    --output-file metrics.json
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_metrics_log_analyzer.py
```

## License
MIT License