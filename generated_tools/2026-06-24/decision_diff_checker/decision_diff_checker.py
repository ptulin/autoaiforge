import argparse
import json
from difflib import unified_diff
from rich.console import Console
from rich.text import Text

def load_json_file(file_path):
    """Load a JSON file and return its content."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise ValueError(f"File not found: {file_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in file: {file_path}")

def generate_diff(old_data, new_data):
    """Generate a unified diff between two JSON objects."""
    old_lines = json.dumps(old_data, indent=4).splitlines(keepends=True)
    new_lines = json.dumps(new_data, indent=4).splitlines(keepends=True)
    diff = unified_diff(old_lines, new_lines, fromfile='old_run', tofile='new_run', lineterm='')
    return list(diff)

def display_diff(diff):
    """Display the diff using rich for better readability."""
    console = Console()
    if not diff:
        console.print("[green]No differences found![/green]")
    else:
        for line in diff:
            if line.startswith('+') and not line.startswith('+++'):
                console.print(Text(line, style="green"))
            elif line.startswith('-') and not line.startswith('---'):
                console.print(Text(line, style="red"))
            else:
                console.print(Text(line))

def main():
    parser = argparse.ArgumentParser(description="Decision Diff Checker: Compare AI decision-making logs.")
    parser.add_argument('--old_run', required=True, help="Path to the old run JSON file.")
    parser.add_argument('--new_run', required=True, help="Path to the new run JSON file.")
    args = parser.parse_args()

    try:
        old_data = load_json_file(args.old_run)
        new_data = load_json_file(args.new_run)
        diff = generate_diff(old_data, new_data)
        display_diff(diff)
    except ValueError as e:
        Console().print(f"[red]Error:[/red] {e}")

if __name__ == "__main__":
    main()
