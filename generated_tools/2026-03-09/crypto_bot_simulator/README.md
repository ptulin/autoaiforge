# Crypto Bot Simulator

## Description
A CLI tool for simulating AI-based trading strategies on historical cryptocurrency data. This tool allows developers to test and evaluate performance metrics for their trading algorithms without risking real money.

## Installation

Install the required Python packages:

```bash
pip install pandas numpy matplotlib
```

## Usage

Run the tool using the following command:

```bash
python crypto_bot_simulator.py --data <path_to_csv> --strategy mean_reversion --output <output_file> --window <window_size> --threshold <z_score_threshold>
```

### Arguments

- `--data`: Path to the historical cryptocurrency data CSV file.
- `--strategy`: Trading strategy to simulate (currently supports `mean_reversion`).
- `--output`: Output file for the results plot (default: `simulation_results.png`).
- `--window`: Rolling window size for the strategy (default: `20`).
- `--threshold`: Z-score threshold for mean reversion (default: `0.01`).

## Example

```bash
python crypto_bot_simulator.py --data historical_data.csv --strategy mean_reversion --output results.png --window 20 --threshold 0.01
```

## Testing

Run the tests using pytest:

```bash
pytest test_crypto_bot_simulator.py
```

## License

MIT License