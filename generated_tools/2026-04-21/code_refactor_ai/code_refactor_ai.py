import os
import argparse
import openai
from rich.console import Console
from rich.table import Table

def analyze_and_refactor_code(file_path, apply_changes):
    """Analyze and refactor Python code using OpenAI models."""
    try:
        with open(file_path, 'r') as file:
            code_content = file.read()

        # Call OpenAI API to analyze and refactor code
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python code refactoring assistant."},
                {"role": "user", "content": f"Analyze and refactor the following Python code:\n{code_content}"}
            ]
        )

        suggestions = response['choices'][0]['message']['content']

        if apply_changes:
            with open(file_path, 'w') as file:
                file.write(suggestions)
            return "Changes applied successfully."
        else:
            return suggestions

    except FileNotFoundError:
        return "Error: File not found."
    except openai.error.OpenAIError as e:
        return f"Error: Failed to communicate with OpenAI API. Details: {str(e)}"

def process_directory(directory_path, apply_changes):
    """Process all Python files in a directory."""
    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                results[file_path] = analyze_and_refactor_code(file_path, apply_changes)
    return results

def main():
    parser = argparse.ArgumentParser(description="Code Refactor AI: AI-powered Python code refactoring tool.")
    parser.add_argument('--input', required=True, help="Path to a Python file or directory.")
    parser.add_argument('--apply', action='store_true', help="Apply changes directly to the code.")
    args = parser.parse_args()

    console = Console()

    if os.path.isfile(args.input):
        result = analyze_and_refactor_code(args.input, args.apply)
        console.print(result)
    elif os.path.isdir(args.input):
        results = process_directory(args.input, args.apply)
        table = Table(title="Refactoring Results")
        table.add_column("File", justify="left", style="cyan")
        table.add_column("Result", justify="left", style="green")

        for file, result in results.items():
            table.add_row(file, result)

        console.print(table)
    else:
        console.print("[red]Error: Invalid input path. Please provide a valid file or directory.[/red]")

if __name__ == "__main__":
    main()