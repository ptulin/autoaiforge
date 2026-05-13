import argparse
import json
import csv
from datetime import datetime
from tabulate import tabulate
import requests

def fetch_memory_data(api_url):
    """Fetch memory data from the given API URL."""
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to fetch memory data: {e}")

def filter_memory_data(memory_data, keyword=None, since=None):
    """Filter memory data based on keyword and timestamp."""
    filtered_data = []
    for entry in memory_data:
        if keyword and keyword.lower() not in entry.get('content', '').lower():
            continue
        if since:
            try:
                entry_time = datetime.strptime(entry.get('timestamp', ''), '%Y-%m-%dT%H:%M:%S')
                if entry_time < since:
                    continue
            except (ValueError, TypeError):
                continue
        filtered_data.append(entry)
    return filtered_data

def display_memory_table(memory_data):
    """Display memory data in a tabular format."""
    headers = ["ID", "Timestamp", "Content"]
    table_data = [[entry.get('id'), entry.get('timestamp'), entry.get('content')] for entry in memory_data]
    return tabulate(table_data, headers=headers, tablefmt="grid")

def export_memory_data(memory_data, output_format, output_file):
    """Export memory data to JSON or CSV."""
    if output_format == 'json':
        with open(output_file, 'w') as f:
            json.dump(memory_data, f, indent=4)
    elif output_format == 'csv':
        with open(output_file, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'content'])
            writer.writeheader()
            writer.writerows(memory_data)
    else:
        raise ValueError("Unsupported output format. Use 'json' or 'csv'.")

def main():
    parser = argparse.ArgumentParser(description="Claude Memory Visualizer")
    parser.add_argument('--api-url', required=True, help="API URL to fetch memory data")
    parser.add_argument('--filter', help="Keyword to filter memory entries")
    parser.add_argument('--since', help="Filter entries since a specific timestamp (YYYY-MM-DD)")
    parser.add_argument('--output', help="Output format (json/csv)")
    parser.add_argument('--output-file', help="Output file path for exported data")

    args = parser.parse_args()

    try:
        memory_data = fetch_memory_data(args.api_url)

        since_date = None
        if args.since:
            try:
                since_date = datetime.strptime(args.since, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format for --since. Use YYYY-MM-DD.")

        filtered_data = filter_memory_data(memory_data, keyword=args.filter, since=since_date)

        if args.output:
            if not args.output_file:
                raise ValueError("--output-file is required when specifying --output.")
            export_memory_data(filtered_data, args.output, args.output_file)
            print(f"Memory data exported to {args.output_file} in {args.output} format.")
        else:
            print(display_memory_table(filtered_data))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()