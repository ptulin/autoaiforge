import argparse
import requests
from pathlib import Path
import json

def analyze_code(file_path, api_url):
    """Send a code file to the Claude AI API for analysis."""
    try:
        with open(file_path, 'r') as file:
            code_content = file.read()
    except FileNotFoundError:
        return {"error": f"File not found: {file_path}"}
    except Exception as e:
        return {"error": f"Error reading file {file_path}: {str(e)}"}

    try:
        response = requests.post(api_url, json={"code": code_content})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}

def process_path(input_path, api_url):
    """Process a file or directory and analyze code files."""
    path = Path(input_path)
    if not path.exists():
        return {"error": f"Path does not exist: {input_path}"}

    results = {}
    if path.is_file():
        results[path.name] = analyze_code(path, api_url)
    elif path.is_dir():
        for file in path.rglob("*.py"):
            results[file.name] = analyze_code(file, api_url)
    else:
        return {"error": f"Invalid path type: {input_path}"}

    return results

def save_report(results, output_file):
    """Save the analysis results to a JSON file."""
    try:
        with open(output_file, 'w') as file:
            json.dump(results, file, indent=4)
    except Exception as e:
        print(f"Error saving report: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Claude Code Reviewer")
    parser.add_argument('--path', required=True, help="Path to a file or directory to analyze")
    parser.add_argument('--api-url', required=True, help="Claude AI API endpoint URL")
    parser.add_argument('--output', help="Output file to save the review report")

    args = parser.parse_args()

    results = process_path(args.path, args.api_url)

    if args.output:
        save_report(results, args.output)
        print(f"Analysis report saved to {args.output}")
    else:
        print(json.dumps(results, indent=4))

if __name__ == "__main__":
    main()