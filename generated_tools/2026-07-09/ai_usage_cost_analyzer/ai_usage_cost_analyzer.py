import argparse
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_pricing_model(pricing_model_path):
    """Load the pricing model from a JSON file."""
    try:
        with open(pricing_model_path, 'r') as file:
            pricing_model = json.load(file)
        return pricing_model
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise ValueError(f"Error loading pricing model: {e}")

def load_usage_logs(log_file_path):
    """Load the usage logs from a JSON or CSV file."""
    try:
        if log_file_path.endswith('.json'):
            return pd.read_json(log_file_path)
        elif log_file_path.endswith('.csv'):
            return pd.read_csv(log_file_path)
        else:
            raise ValueError("Unsupported file format. Use JSON or CSV.")
    except (FileNotFoundError, ValueError) as e:
        raise ValueError(f"Error loading usage logs: {e}")

def calculate_costs(usage_logs, pricing_model):
    """Calculate the costs based on the usage logs and pricing model."""
    if 'api_name' not in usage_logs.columns or 'usage_count' not in usage_logs.columns:
        raise ValueError("Usage logs must contain 'api_name' and 'usage_count' columns.")

    def calculate_row_cost(row):
        api_name = row['api_name']
        usage_count = row['usage_count']
        if api_name not in pricing_model:
            raise ValueError(f"API '{api_name}' not found in pricing model.")
        cost_per_call = pricing_model[api_name].get('cost_per_call', 0)
        return usage_count * cost_per_call

    usage_logs['cost'] = usage_logs.apply(calculate_row_cost, axis=1)
    return usage_logs

def generate_report(usage_logs, output_file=None):
    """Generate a cost breakdown report and optionally save it to a CSV file."""
    total_cost = usage_logs['cost'].sum()
    cost_breakdown = usage_logs.groupby('api_name')['cost'].sum().reset_index()

    print("\n--- Cost Breakdown Report ---")
    print(cost_breakdown)
    print(f"\nTotal Cost: ${total_cost:.2f}")

    if output_file:
        cost_breakdown.to_csv(output_file, index=False)
        print(f"\nReport saved to {output_file}")

def plot_cost_breakdown(usage_logs):
    """Generate a bar chart for the cost breakdown."""
    cost_breakdown = usage_logs.groupby('api_name')['cost'].sum()
    cost_breakdown.plot(kind='bar', title='Cost Breakdown by API', ylabel='Cost ($)', xlabel='API Name')
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser(description="AI Usage Cost Analyzer")
    parser.add_argument('--log-file', required=True, help="Path to the API usage log file (JSON or CSV).")
    parser.add_argument('--pricing-model', required=True, help="Path to the pricing model JSON file.")
    parser.add_argument('--output-file', help="Optional path to save the cost breakdown report as a CSV.")
    parser.add_argument('--plot', action='store_true', help="Generate a bar chart for the cost breakdown.")

    args = parser.parse_args()

    try:
        pricing_model = load_pricing_model(args.pricing_model)
        usage_logs = load_usage_logs(args.log_file)
        usage_logs_with_costs = calculate_costs(usage_logs, pricing_model)
        generate_report(usage_logs_with_costs, args.output_file)

        if args.plot:
            plot_cost_breakdown(usage_logs_with_costs)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()