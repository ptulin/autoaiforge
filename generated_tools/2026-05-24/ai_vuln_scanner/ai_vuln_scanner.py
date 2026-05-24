import os
import json
import argparse
from rich.console import Console
from rich.table import Table
import openai

# Initialize the rich console
console = Console()

def scan_file(file_path):
    """Scan a single file for vulnerabilities using an AI model."""
    try:
        with open(file_path, 'r') as file:
            code_content = file.read()

        # Simulate AI model call (replace with actual OpenAI API call)
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following code for security vulnerabilities and provide suggestions:\n{code_content}",
            max_tokens=500
        )

        return response['choices'][0]['text'].strip()

    except Exception as e:
        console.print(f"[red]Error scanning file {file_path}: {e}")
        return None

def scan_directory(directory_path):
    """Scan all files in a directory for vulnerabilities."""
    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.py', '.js', '.java', '.c', '.cpp')):  # Example extensions
                console.print(f"Scanning file: {file_path}")
                result = scan_file(file_path)
                if result:
                    results[file_path] = result
    return results

def generate_report(results, output_file=None):
    """Generate a report from the scan results."""
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
        console.print(f"[green]Report saved to {output_file}")
    else:
        table = Table(title="Vulnerability Report")
        table.add_column("File", style="cyan")
        table.add_column("Issues", style="magenta")

        for file, issues in results.items():
            table.add_row(file, issues)

        console.print(table)

def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Vulnerability Scanner: Scan source code files or directories for vulnerabilities using AI."
    )
    parser.add_argument(
        '--path',
        type=str,
        required=True,
        help="Path to the file or directory to scan."
    )
    parser.add_argument(
        '--output',
        type=str,
        help="Optional output file to save the report (JSON format)."
    )

    args = parser.parse_args()

    if not os.path.exists(args.path):
        console.print(f"[red]Error: The path {args.path} does not exist.")
        return

    if os.path.isfile(args.path):
        console.print(f"Scanning file: {args.path}")
        result = scan_file(args.path)
        if result:
            results = {args.path: result}
            generate_report(results, args.output)
    elif os.path.isdir(args.path):
        console.print(f"Scanning directory: {args.path}")
        results = scan_directory(args.path)
        generate_report(results, args.output)
    else:
        console.print(f"[red]Error: The path {args.path} is neither a file nor a directory.")

if __name__ == "__main__":
    main()