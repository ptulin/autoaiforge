# AI Strategy Simulator

AI Strategy Simulator is a command-line tool that enables users to test and refine trading strategies using historical market data. It integrates AI-powered predictive models to analyze trends and evaluate the performance of custom strategies over chosen time periods.

## Features
- Load historical market data from CSV files
- Apply AI-based predictive models (e.g., linear regression)
- Simulate trading strategies (e.g., buy low, sell high)
- Visualize strategy performance metrics (e.g., profit, drawdown)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ai_strategy_simulator.git
   cd ai_strategy_simulator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python ai_strategy_simulator.py --data market_data.csv --model linear_regression --strategy buy_low_sell_high --output performance.png
```

### Arguments
- `--data`: Path to the CSV file containing market data (must include `Date` and `Price` columns)
- `--model`: AI model to use (currently supports `linear_regression`)
- `--strategy`: Trading strategy to simulate (currently supports `buy_low_sell_high`)
- `--output`: Output file for the performance chart (default: `performance.png`)

## Example

```bash
python ai_strategy_simulator.py --data market_data.csv --model linear_regression --strategy buy_low_sell_high
```

## License

This project is licensed under the MIT License.
