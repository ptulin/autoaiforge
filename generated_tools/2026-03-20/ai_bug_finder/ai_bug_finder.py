import os
import openai
import click
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_code_with_ai(file_content):
    """
    Sends the content of a Python file to OpenAI's API for analysis.

    Args:
        file_content (str): The content of the Python file.

    Returns:
        list: A list of dictionaries containing bug details and suggestions.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python code analysis assistant."},
                {"role": "user", "content": f"Analyze the following Python code for bugs and suggest fixes:\n\n{file_content}"}
            ]
        )
        suggestions = response['choices'][0]['message']['content']
        return suggestions
    except Exception as e:
        console.print(f"[red]Error communicating with OpenAI API: {e}[/red]")
        return None

def scan_file(file_path):
    """
    Scans a single Python file for potential bugs using AI.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: A dictionary containing file analysis results.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        suggestions = analyze_code_with_ai(content)
        return {"file": file_path, "suggestions": suggestions}
    except Exception as e:
        console.print(f"[red]Error reading file {file_path}: {e}[/red]")
        return {"file": file_path, "suggestions": None}

def scan_directory(directory_path):
    """
    Scans all Python files in a directory for potential bugs using AI.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        list: A list of dictionaries containing analysis results for each file.
    """
    results = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                results.append(scan_file(file_path))
    return results

def display_results(results):
    """
    Displays the analysis results in a readable format.

    Args:
        results (list): List of analysis results.
    """
    table = Table(title="AI Bug Finder Results")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Suggestions", style="magenta")

    for result in results:
        suggestions = result['suggestions'] or "No suggestions or failed to analyze."
        table.add_row(result['file'], suggestions)

    console.print(table)

@click.command()
@click.option('--path', required=True, type=click.Path(exists=True), help="Path to a Python file or directory.")
def main(path):
    """
    Main entry point for the AI Bug Finder CLI tool.

    Args:
        path (str): Path to the file or directory to analyze.
    """
    if os.path.isfile(path):
        results = [scan_file(path)]
    elif os.path.isdir(path):
        results = scan_directory(path)
    else:
        console.print("[red]Invalid path provided. Please provide a valid file or directory path.[/red]")
        return

    display_results(results)

if __name__ == "__main__":
    main()
