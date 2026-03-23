# AI Backtesting Toolkit

## Overview
The AI Backtesting Toolkit is a Python library designed to help developers backtest AI-driven trading strategies using historical market data. It provides evaluation metrics such as ROI and Sharpe Ratio, along with visualizations to optimize algorithms before deploying them in live scenarios.

## Features
- Backtest trading strategies using historical market data.
- Calculate performance metrics such as ROI and Sharpe Ratio.
- Generate visualizations for buy/sell signals and market prices.

## Installation
Install the required dependencies:

```bash
pip install pandas numpy matplotlib pytest
```

## Usage
Run the toolkit via the command line:

```bash
python ai_backtesting_toolkit.py <strategy_module_path> <data_csv_path>
```

### Arguments
- `strategy_module_path`: Path to the Python module containing the strategy function.
- `data_csv_path`: Path to the CSV file containing historical market data.

### Example
Create a strategy module `my_strategy.py`:

```python
def strategy(data):
    trades = data.copy()
    trades["action"] = "hold"
    trades.loc[trades.index[::10], "action"] = "buy"
    trades.loc[trades.index[5::10], "action"] = "sell"
    return trades
```

Run the backtest:

```bash
python ai_backtesting_toolkit.py my_strategy.py historical_data.csv
```

## Testing
Run the tests using pytest:

```bash
pytest test_ai_backtesting_toolkit.py
```

## License
MIT License