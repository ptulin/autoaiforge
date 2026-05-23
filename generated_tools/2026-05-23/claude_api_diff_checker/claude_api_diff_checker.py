import argparse
import json
import os
from urllib.parse import urlparse
import requests
import jsondiff

def load_json(source):
    """
    Load JSON data from a file or URL.
    """
    if urlparse(source).scheme in ('http', 'https'):
        try:
            response = requests.get(source)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise ValueError(f"Failed to fetch JSON from URL: {e}")
    else:
        if not os.path.exists(source):
            raise ValueError(f"File not found: {source}")
        try:
            with open(source, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}")

def generate_diff(old_data, new_data):
    """
    Generate a diff between two JSON objects using jsondiff.
    """
    return jsondiff.diff(old_data, new_data)

def export_diff(diff, output_format):
    """
    Export the diff in the specified format (markdown or JSON).
    """
    if output_format == 'json':
        return json.dumps(diff, indent=4)
    elif output_format == 'markdown':
        markdown_lines = ["# API Diff Report\n"]
        markdown_lines.append("```json")
        markdown_lines.append(json.dumps(diff, indent=4))
        markdown_lines.append("```")
        return "\n".join(markdown_lines)
    else:
        raise ValueError("Unsupported format. Use 'json' or 'markdown'.")

def main():
    parser = argparse.ArgumentParser(description="Claude API Diff Checker")
    parser.add_argument('--old', required=True, help="Path or URL to the old API documentation (JSON)")
    parser.add_argument('--new', required=True, help="Path or URL to the new API documentation (JSON)")
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown', help="Output format for the diff report")
    args = parser.parse_args()

    try:
        old_data = load_json(args.old)
        new_data = load_json(args.new)
        diff = generate_diff(old_data, new_data)
        report = export_diff(diff, args.format)
        print(report)
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()