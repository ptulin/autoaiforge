# AI Cost Analyzer

## Overview
AI Cost Analyzer is a Python tool designed for retrospective analysis of AI agent token usage and API costs. It processes API logs, calculates usage metrics, identifies trends, and generates visual reports to help developers optimize their workflows and reduce costs.

## Features
- Load API usage logs in CSV or JSON format.
- Analyze token usage and calculate daily cost metrics.
- Generate visual reports in PDF format.

## Installation
Install the required dependencies using pip:

```bash
pip install pandas matplotlib
```

## Usage
Run the tool from the command line:

```bash
python ai_cost_analyzer.py --input <input_file> --output <output_file>
```

### Arguments
- `--input`: Path to the input API usage log file (CSV or JSON).
- `--output`: Path to the output report file (PDF).

## Example
```bash
python ai_cost_analyzer.py --input usage_logs.csv --output report.pdf
```

## Testing
Run the tests using pytest:

```bash
pytest test_ai_cost_analyzer.py
```

## License
This project is licensed under the MIT License.