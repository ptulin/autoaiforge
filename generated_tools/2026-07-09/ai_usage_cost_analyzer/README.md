# AI Usage Cost Analyzer

## Description
The AI Usage Cost Analyzer is a Python-based tool designed to analyze logs of API usage and calculate the associated costs based on a customizable pricing model. This tool helps businesses understand their AI usage costs and identify high-cost patterns in their operations.

## Features
- Parses API usage logs in JSON or CSV format.
- Supports customizable pricing model input (e.g., cost per API call, tiered pricing).
- Generates detailed cost breakdown reports.
- Optionally saves the report as a CSV file.
- Provides an option to generate a bar chart for visualizing cost breakdown.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_usage_cost_analyzer.git
   cd ai_usage_cost_analyzer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command-line Arguments
- `--log-file`: Path to the API usage log file (JSON or CSV). (Required)
- `--pricing-model`: Path to the pricing model JSON file. (Required)
- `--output-file`: Optional path to save the cost breakdown report as a CSV.
- `--plot`: Generate a bar chart for the cost breakdown.

### Example

```bash
python ai_usage_cost_analyzer.py --log-file usage_logs.json --pricing-model pricing_config.json --output-file cost_report.csv --plot
```

## Example Input Files

### Usage Logs (JSON or CSV)
```json
[
  {"api_name": "api1", "usage_count": 100},
  {"api_name": "api2", "usage_count": 200}
]
```

### Pricing Model (JSON)
```json
{
  "api1": {"cost_per_call": 0.01},
  "api2": {"cost_per_call": 0.02}
}
```

## Output
- A detailed cost breakdown report printed to the console.
- Optionally, a CSV file containing the cost breakdown.
- A bar chart visualizing the cost breakdown (if `--plot` is used).

## Testing

Run the tests using `pytest`:

```bash
pytest test_ai_usage_cost_analyzer.py
```

The test suite includes tests for:
- Loading the pricing model.
- Loading usage logs from JSON and CSV files.
- Calculating costs based on the pricing model.

## License
This project is licensed under the MIT License.
