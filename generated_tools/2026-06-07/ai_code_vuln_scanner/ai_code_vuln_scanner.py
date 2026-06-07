import os
import argparse
from transformers import pipeline
from tqdm import tqdm
from rich.console import Console
from rich.table import Table

def scan_file(file_path, ai_model):
    """
    Scans a single Python file for vulnerabilities using the AI model.

    Args:
        file_path (str): Path to the Python file.
        ai_model: Pre-trained AI model for vulnerability detection.

    Returns:
        list: List of detected vulnerabilities with line numbers and suggestions.
    """
    vulnerabilities = []
    try:
        with open(file_path, 'r') as file:
            code = file.read()
            results = ai_model(code)
            for result in results:
                vulnerabilities.append({
                    'line': result['line'],
                    'issue': result['issue'],
                    'suggestion': result['suggestion']
                })
    except Exception as e:
        vulnerabilities.append({
            'line': None,
            'issue': f"Error reading file: {e}",
            'suggestion': "Ensure the file is accessible and properly formatted."
        })
    return vulnerabilities

def scan_directory(directory_path, ai_model):
    """
    Scans all Python files in a directory for vulnerabilities using the AI model.

    Args:
        directory_path (str): Path to the directory.
        ai_model: Pre-trained AI model for vulnerability detection.

    Returns:
        dict: Dictionary with file paths as keys and vulnerability lists as values.
    """
    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                results[file_path] = scan_file(file_path, ai_model)
    return results

def main():
    parser = argparse.ArgumentParser(description="AI Code Vulnerability Scanner")
    parser.add_argument('--path', type=str, required=True, help="Path to a Python file or directory to scan.")
    args = parser.parse_args()

    console = Console()
    ai_model = pipeline('text-classification', model='secure-coding/vuln-scanner')

    if os.path.isfile(args.path):
        console.print(f"[bold green]Scanning file:[/bold green] {args.path}")
        vulnerabilities = scan_file(args.path, ai_model)
        display_results({args.path: vulnerabilities}, console)
    elif os.path.isdir(args.path):
        console.print(f"[bold green]Scanning directory:[/bold green] {args.path}")
        results = scan_directory(args.path, ai_model)
        display_results(results, console)
    else:
        console.print(f"[bold red]Error:[/bold red] The path {args.path} does not exist.")

def display_results(results, console):
    """
    Displays the scan results in a human-readable format.

    Args:
        results (dict): Dictionary of scan results.
        console (Console): Rich console for output.
    """
    for file_path, vulnerabilities in results.items():
        console.print(f"\n[bold blue]File:[/bold blue] {file_path}")
        if not vulnerabilities:
            console.print("[green]No vulnerabilities found![/green]")
        else:
            table = Table(title="Vulnerabilities")
            table.add_column("Line", justify="center")
            table.add_column("Issue", justify="left")
            table.add_column("Suggestion", justify="left")
            for vuln in vulnerabilities:
                table.add_row(
                    str(vuln['line']) if vuln['line'] else "N/A",
                    vuln['issue'],
                    vuln['suggestion']
                )
            console.print(table)

if __name__ == "__main__":
    main()