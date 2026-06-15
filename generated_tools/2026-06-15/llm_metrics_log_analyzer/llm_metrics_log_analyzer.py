import argparse
import re
import json
import pandas as pd
from pathlib import Path


def parse_logs(log_file, log_format):
    """
    Parses the log file and extracts metrics based on the provided log format.

    Args:
        log_file (str): Path to the log file.
        log_format (str): Regex pattern to parse the log entries.

    Returns:
        pd.DataFrame: A DataFrame containing parsed log data.
    """
    pattern = re.compile(log_format)
    data = []

    with open(log_file, 'r') as file:
        for line in file:
            match = pattern.match(line)
            if match:
                data.append(match.groupdict())

    if not data:
        raise ValueError("No valid log entries found in the file.")

    return pd.DataFrame(data)


def analyze_metrics(df):
    """
    Analyzes metrics from the parsed log data.

    Args:
        df (pd.DataFrame): DataFrame containing parsed log data.

    Returns:
        dict: Aggregated metrics.
    """
    df['latency'] = pd.to_numeric(df['latency'], errors='coerce')
    df['tokens'] = pd.to_numeric(df['tokens'], errors='coerce')

    metrics = {
        'average_latency': df['latency'].mean(),
        'total_tokens': df['tokens'].sum(),
        'error_count': df['status'].str.contains('error', case=False, na=False).sum()
    }

    return metrics


def save_output(metrics, output_format, output_file):
    """
    Saves the aggregated metrics to the specified output format.

    Args:
        metrics (dict): Aggregated metrics.
        output_format (str): Output format (json, csv, console).
        output_file (str): Path to save the output file.
    """
    if output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(metrics, f, indent=4)
    elif output_format == 'csv':
        pd.DataFrame([metrics]).to_csv(output_file, index=False)
    elif output_format == 'console':
        print(json.dumps(metrics, indent=4))
    else:
        raise ValueError("Unsupported output format. Choose from 'json', 'csv', or 'console'.")


def main():
    parser = argparse.ArgumentParser(description="LLM Metrics Log Analyzer")
    parser.add_argument('--log-file', required=True, help="Path to the log file.")
    parser.add_argument('--log-format', required=True, help="Regex pattern to parse the log entries.")
    parser.add_argument('--output-format', choices=['json', 'csv', 'console'], default='console', help="Output format (default: console).")
    parser.add_argument('--output-file', help="Path to save the output file (required for json/csv output).")

    args = parser.parse_args()

    if args.output_format in ['json', 'csv'] and not args.output_file:
        parser.error("--output-file is required for json/csv output.")

    try:
        df = parse_logs(args.log_file, args.log_format)
        metrics = analyze_metrics(df)
        save_output(metrics, args.output_format, args.output_file)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()