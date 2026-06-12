import argparse
import pandas as pd
import matplotlib.pyplot as plt
import json
from io import StringIO

def load_data(input_file):
    """Load data from a CSV or JSON file."""
    try:
        if input_file.endswith('.csv'):
            with open(input_file, 'r') as f:
                return pd.read_csv(f)
        elif input_file.endswith('.json'):
            with open(input_file, 'r') as f:
                return pd.read_json(f)
        else:
            raise ValueError("Unsupported file format. Please use CSV or JSON.")
    except Exception as e:
        raise ValueError(f"Error loading file: {e}")

def analyze_usage(data):
    """Analyze token usage and calculate cost metrics."""
    if 'timestamp' not in data.columns or 'tokens' not in data.columns or 'cost' not in data.columns:
        raise ValueError("Input data must contain 'timestamp', 'tokens', and 'cost' columns.")

    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data.set_index('timestamp', inplace=True)

    # Calculate daily token usage and cost
    daily_stats = data.resample('D').sum()

    return daily_stats

def generate_report(daily_stats, output_file):
    """Generate a report with visualizations and save it as a PDF."""
    try:
        plt.figure(figsize=(10, 6))

        # Plot token usage
        plt.subplot(2, 1, 1)
        plt.plot(daily_stats.index, daily_stats['tokens'], marker='o', label='Token Usage')
        plt.title('Daily Token Usage')
        plt.xlabel('Date')
        plt.ylabel('Tokens')
        plt.legend()

        # Plot cost
        plt.subplot(2, 1, 2)
        plt.plot(daily_stats.index, daily_stats['cost'], marker='o', color='red', label='Cost')
        plt.title('Daily Cost')
        plt.xlabel('Date')
        plt.ylabel('Cost (USD)')
        plt.legend()

        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()
    except Exception as e:
        raise ValueError(f"Error generating report: {e}")

def main():
    parser = argparse.ArgumentParser(description='AI Cost Analyzer: Analyze token usage and API costs.')
    parser.add_argument('--input', required=True, help='Path to the input API usage log file (CSV or JSON).')
    parser.add_argument('--output', required=True, help='Path to the output report file (PDF).')
    args = parser.parse_args()

    try:
        # Load data
        data = load_data(args.input)

        # Analyze usage
        daily_stats = analyze_usage(data)

        # Generate report
        generate_report(daily_stats, args.output)

        print(f"Report successfully generated: {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()