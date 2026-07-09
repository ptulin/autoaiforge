# AI Cost Forecaster

## Description
AI Cost Forecaster is a CLI tool that predicts future AI usage costs based on historical API call data. It uses statistical and machine learning models to provide forecasts, helping businesses plan budgets and optimize costs.

## Features
- Reads historical usage data in CSV or JSON format
- Supports linear regression and ARIMA for time-series forecasting
- Provides visualizations of predicted costs
- Optionally saves forecast data to a CSV file

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ai_cost_forecaster.py --input-file usage_data.csv --forecast-horizon 7 --method linear --output-file forecast.csv
```

### Arguments
- `--input-file`: Path to the input file (CSV or JSON).
- `--forecast-horizon`: Number of days to forecast (default: 7).
- `--method`: Forecasting method (`linear` or `arima`, default: `linear`).
- `--output-file`: Optional path to save the forecast as a CSV file.

## Example

```bash
python ai_cost_forecaster.py --input-file usage_data.csv --forecast-horizon 7
```

## License
MIT License