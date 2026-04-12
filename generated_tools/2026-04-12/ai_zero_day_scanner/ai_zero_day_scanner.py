import os
import argparse
from transformers import pipeline
from rich.console import Console
from rich.table import Table
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

# Initialize Rich console
console = Console()

def analyze_code(file_path):
    """Analyze a single file for vulnerabilities."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        with open(file_path, 'r') as f:
            code = f.read()
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")

    # Mockable AI model pipeline for code analysis
    vulnerability_detector = pipeline("text-classification", model="distilbert-base-uncased")

    # Analyze the code
    results = vulnerability_detector(code, truncation=True)

    return results

def generate_report(results, output_path=None):
    """Generate a vulnerability report."""
    table = Table(title="Vulnerability Report")
    table.add_column("Line", justify="right", style="cyan")
    table.add_column("Severity", style="magenta")
    table.add_column("Description", style="white")

    for result in results:
        table.add_row(str(result.get('line', 'N/A')), result['label'], str(result['score']))

    if output_path:
        try:
            with open(output_path, 'w') as f:
                f.write(str(table))
        except Exception as e:
            raise RuntimeError(f"Error writing report to {output_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Zero-Day Scanner")
    parser.add_argument('--path', required=True, help="Path to file or directory to scan")
    parser.add_argument('--output', help="Path to save the output report")

    args = parser.parse_args()

    if os.path.isdir(args.path):
        files = [os.path.join(args.path, f) for f in os.listdir(args.path) if f.endswith('.py')]
    else:
        files = [args.path]

    all_results = []
    for file in files:
        try:
            console.print(f"Analyzing {file}...", style="bold green")
            results = analyze_code(file)
            all_results.extend(results)
        except Exception as e:
            console.print(f"Error analyzing {file}: {e}", style="bold red")

    if all_results:
        generate_report(all_results, args.output)
        console.print("Vulnerability report generated successfully.", style="bold green")
    else:
        console.print("No vulnerabilities found or no files analyzed.", style="bold yellow")