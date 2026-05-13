import argparse
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import os

def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        if 'Date' in data.columns and 'Price' in data.columns:
            data['Date'] = pd.to_datetime(data['Date'])
            return data
        else:
            raise ValueError("CSV must contain 'Date' and 'Price' columns.")
    except Exception as e:
        raise ValueError(f"Error loading data: {e}")

def apply_strategy(data, model_type, strategy):
    if model_type == 'linear_regression':
        model = LinearRegression()
        data['Day'] = np.arange(len(data))
        model.fit(data[['Day']], data['Price'])
        data['Predicted'] = model.predict(data[['Day']])
    else:
        raise ValueError("Unsupported model type. Only 'linear_regression' is supported.")

    if strategy == 'buy_low_sell_high':
        data['Signal'] = (data['Price'] < data['Predicted']).astype(int)
    else:
        raise ValueError("Unsupported strategy. Only 'buy_low_sell_high' is supported.")

    return data

def evaluate_performance(data):
    data['Daily Return'] = data['Price'].pct_change()
    data['Strategy Return'] = data['Signal'].shift(1) * data['Daily Return']
    cumulative_strategy_return = (1 + data['Strategy Return'].fillna(0)).cumprod()
    cumulative_market_return = (1 + data['Daily Return'].fillna(0)).cumprod()
    return cumulative_strategy_return, cumulative_market_return

def visualize_performance(data, cumulative_strategy_return, cumulative_market_return, output_file):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Date'], cumulative_strategy_return, label='Strategy Return')
    plt.plot(data['Date'], cumulative_market_return, label='Market Return')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.legend()
    plt.title('Strategy vs Market Performance')
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description='AI Strategy Simulator')
    parser.add_argument('--data', required=True, help='Path to the CSV file containing market data')
    parser.add_argument('--model', required=True, choices=['linear_regression'], help='AI model to use')
    parser.add_argument('--strategy', required=True, choices=['buy_low_sell_high'], help='Trading strategy to simulate')
    parser.add_argument('--output', default='performance.png', help='Output file for the performance chart')

    args = parser.parse_args()

    try:
        data = load_data(args.data)
        data = apply_strategy(data, args.model, args.strategy)
        cumulative_strategy_return, cumulative_market_return = evaluate_performance(data)
        visualize_performance(data, cumulative_strategy_return, cumulative_market_return, args.output)
        print(f"Simulation completed. Performance chart saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()