import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_data(file_path):
    """Load and preprocess historical cryptocurrency data."""
    try:
        data = pd.read_csv(file_path)
        if 'price' not in data.columns or 'timestamp' not in data.columns:
            raise ValueError("CSV must contain 'timestamp' and 'price' columns.")
        data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')
        if data['timestamp'].isnull().any():
            raise ValueError("Error loading data: Invalid timestamp format.")
        data.sort_values('timestamp', inplace=True)
        data.reset_index(drop=True, inplace=True)
        return data
    except pd.errors.EmptyDataError:
        raise ValueError("Error loading data: File is empty or invalid.")
    except pd.errors.ParserError:
        raise ValueError("Error loading data: Failed to parse CSV.")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def mean_reversion_strategy(data, window=20, threshold=0.01):
    """Simulate a mean reversion trading strategy."""
    data['rolling_mean'] = data['price'].rolling(window=window).mean()
    data['rolling_std'] = data['price'].rolling(window=window).std()
    data['z_score'] = (data['price'] - data['rolling_mean']) / data['rolling_std']

    data['position'] = 0
    data.loc[data['z_score'] > threshold, 'position'] = -1  # Sell
    data.loc[data['z_score'] < -threshold, 'position'] = 1  # Buy

    data['strategy_returns'] = data['position'].shift(1) * data['price'].pct_change()
    data['cumulative_returns'] = (1 + data['strategy_returns']).cumprod()

    return data

def plot_results(data, output_file):
    """Plot the trading strategy results."""
    plt.figure(figsize=(12, 6))
    plt.plot(data['timestamp'], data['cumulative_returns'], label='Strategy Returns')
    plt.xlabel('Timestamp')
    plt.ylabel('Cumulative Returns')
    plt.title('Trading Strategy Simulation')
    plt.legend()
    plt.grid()
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Crypto Bot Simulator")
    parser.add_argument('--data', required=True, help="Path to historical crypto data CSV file.")
    parser.add_argument('--strategy', required=True, choices=['mean_reversion'], help="Trading strategy to simulate.")
    parser.add_argument('--output', default='simulation_results.png', help="Output file for the results plot.")
    parser.add_argument('--window', type=int, default=20, help="Rolling window size for the strategy.")
    parser.add_argument('--threshold', type=float, default=0.01, help="Z-score threshold for mean reversion.")

    args = parser.parse_args()

    try:
        data = load_data(args.data)

        if args.strategy == 'mean_reversion':
            simulated_data = mean_reversion_strategy(data, window=args.window, threshold=args.threshold)

        plot_results(simulated_data, args.output)

        final_cumulative_return = simulated_data['cumulative_returns'].iloc[-1]
        print(f"Final Cumulative Return: {final_cumulative_return:.2f}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()