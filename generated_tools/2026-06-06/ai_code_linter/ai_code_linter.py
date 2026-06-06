import os
import argparse
import json
from typing import List
from openai import ChatCompletion
from rich.console import Console
from rich.table import Table

def analyze_code(file_content: str, config: dict) -> List[dict]:
    """
    Analyze the given code using OpenAI's API and return issues.

    Args:
        file_content (str): The content of the code file.
        config (dict): Linting configuration.

    Returns:
        List[dict]: A list of issues with recommendations.
    """
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code linter."},
                {"role": "user", "content": f"Analyze this code:\n{file_content}\n\nRules: {json.dumps(config)}"}
            ]
        )
        return json.loads(response['choices'][0]['message']['content'])
    except Exception as e:
        return [{"error": f"Failed to analyze code: {str(e)}"}]

def load_config(config_path: str) -> dict:
    """
    Load linting configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        dict: Configuration dictionary.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    with open(config_path, 'r') as config_file:
        return json.load(config_file)

def process_file(file_path: str, config: dict, console: Console):
    """
    Process a single file for linting.

    Args:
        file_path (str): Path to the file to analyze.
        config (dict): Linting configuration.
        console (Console): Rich console for output.
    """
    if not os.path.exists(file_path):
        console.print(f"[red]File not found: {file_path}[/red]")
        return

    with open(file_path, 'r') as file:
        file_content = file.read()

    console.print(f"Analyzing [bold]{file_path}[/bold]...")
    issues = analyze_code(file_content, config)

    table = Table(title=f"Issues in {file_path}")
    table.add_column("Line", justify="right")
    table.add_column("Issue", justify="left")
    table.add_column("Recommendation", justify="left")

    for issue in issues:
        if "error" in issue:
            console.print(f"[red]{issue['error']}[/red]")
        else:
            table.add_row(str(issue.get("line", "N/A")), issue.get("issue", "N/A"), issue.get("recommendation", "N/A"))

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="AI Code Linter")
    parser.add_argument("--path", required=True, help="Path to file or directory to lint")
    parser.add_argument("--config", required=False, default=None, help="Path to configuration file")

    args = parser.parse_args()

    console = Console()

    # Load configuration
    config = {}
    if args.config:
        try:
            config = load_config(args.config)
        except Exception as e:
            console.print(f"[red]Error loading config: {str(e)}[/red]")
            return

    # Process files
    if os.path.isdir(args.path):
        for root, _, files in os.walk(args.path):
            for file in files:
                if file.endswith(('.py', '.js', '.java', '.cpp')):
                    process_file(os.path.join(root, file), config, console)
    elif os.path.isfile(args.path):
        process_file(args.path, config, console)
    else:
        console.print(f"[red]Invalid path: {args.path}[/red]")

if __name__ == "__main__":
    main()
