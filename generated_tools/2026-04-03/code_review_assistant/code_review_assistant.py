import os
import argparse
import yaml
from rich.console import Console
from rich.table import Table
import openai

# Initialize rich console for pretty printing
console = Console()

def analyze_code(file_content, model="gpt-3.5-turbo", criteria=None):
    """
    Analyze the given Python code using OpenAI's API.

    :param file_content: The content of the Python file to analyze.
    :param model: The OpenAI model to use for analysis.
    :param criteria: Custom review criteria provided by the user.
    :return: Analysis result as a dictionary.
    """
    prompt = """
You are a code review assistant. Analyze the following Python code for potential bugs, performance issues, and best practices.

Code:
{code}

Criteria:
{criteria}

Provide a detailed review report.
""".format(code=file_content, criteria=criteria or "Default criteria")

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        console.print(f"[red]Error communicating with OpenAI API: {e}[/red]")
        return None

def process_file(file_path, model, criteria):
    """
    Process a single Python file for code review.

    :param file_path: Path to the Python file.
    :param model: The OpenAI model to use.
    :param criteria: Custom review criteria.
    :return: Review report as a string.
    """
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            return analyze_code(file_content, model, criteria)
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Error reading file {file_path}: {e}[/red]")
    return None

def process_directory(directory_path, model, criteria):
    """
    Process all Python files in a directory for code review.

    :param directory_path: Path to the directory.
    :param model: The OpenAI model to use.
    :param criteria: Custom review criteria.
    :return: Dictionary of file paths and their respective review reports.
    """
    review_reports = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                console.print(f"[blue]Analyzing {file_path}...[/blue]")
                review_reports[file_path] = process_file(file_path, model, criteria)
    return review_reports

def main():
    parser = argparse.ArgumentParser(
        description="Code Review Assistant: Analyze Python code for bugs, performance issues, and best practices."
    )
    parser.add_argument("--file", type=str, help="Path to a Python file to analyze.")
    parser.add_argument("--dir", type=str, help="Path to a directory containing Python files to analyze.")
    parser.add_argument("--output", type=str, help="Path to save the review report in YAML format.")
    parser.add_argument("--criteria", type=str, help="Custom review criteria.")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="OpenAI model to use for analysis.")

    args = parser.parse_args()

    if not args.file and not args.dir:
        console.print("[red]Error: You must provide either --file or --dir.[/red]")
        parser.print_help()
        return

    if args.file:
        console.print(f"[green]Analyzing file: {args.file}[/green]")
        report = {args.file: process_file(args.file, args.model, args.criteria)}
    elif args.dir:
        console.print(f"[green]Analyzing directory: {args.dir}[/green]")
        report = process_directory(args.dir, args.model, args.criteria)

    if args.output:
        try:
            with open(args.output, "w") as output_file:
                yaml.dump(report, output_file)
            console.print(f"[green]Report saved to {args.output}[/green]")
        except Exception as e:
            console.print(f"[red]Error saving report: {e}[/red]")
    else:
        table = Table(title="Code Review Report")
        table.add_column("File", style="cyan")
        table.add_column("Review", style="magenta")
        for file, review in report.items():
            table.add_row(file, review or "[red]Error analyzing file[/red]")
        console.print(table)

if __name__ == "__main__":
    main()