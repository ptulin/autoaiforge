import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import StringIO

def load_data(input_file):
    """Load data from a CSV or JSON file."""
    if input_file.endswith('.csv'):
        return pd.read_csv(input_file)
    elif input_file.endswith('.json'):
        return pd.read_json(input_file)
    else:
        raise ValueError("Unsupported file format. Please provide a CSV or JSON file.")

def analyze_rewards(data):
    """Analyze reward patterns and return summary statistics."""
    if 'reward' not in data.columns or 'step' not in data.columns:
        raise ValueError("Input data must contain 'reward' and 'step' columns.")

    summary = {
        'total_rewards': data['reward'].sum(),
        'average_reward': data['reward'].mean(),
        'max_reward': data['reward'].max(),
        'min_reward': data['reward'].min(),
        'steps': len(data)
    }
    return summary

def plot_rewards(data, output_file):
    """Generate a plot of rewards over steps."""
    plt.figure(figsize=(10, 6))
    plt.plot(data['step'], data['reward'], marker='o', linestyle='-', color='b')
    plt.title('Reward Attribution Over Time')
    plt.xlabel('Step')
    plt.ylabel('Reward')
    plt.grid(True)
    plt.savefig(output_file)
    plt.close()

def main():
    parser = argparse.ArgumentParser(description="Reward Trace Explorer: Analyze and visualize AI agent reward signals.")
    parser.add_argument('--input', required=True, help="Path to the input CSV or JSON file containing agent data.")
    parser.add_argument('--output', required=True, help="Path to save the output analysis graph.")
    args = parser.parse_args()

    try:
        data = load_data(args.input)
        summary = analyze_rewards(data)
        plot_rewards(data, args.output)

        print("Analysis Summary:")
        for key, value in summary.items():
            print(f"{key}: {value}")
        print(f"Graph saved to {args.output}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()