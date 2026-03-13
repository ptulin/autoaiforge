import argparse
import os
import openai
from black import format_file_in_place, FileMode, WriteBack
from rich.console import Console
from rich.syntax import Syntax
from pathlib import Path

def refactor_code_with_ai(api_key, code):
    """Uses OpenAI API to refactor the given Python code."""
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python code refactoring assistant."},
                {"role": "user", "content": f"Refactor the following Python code for readability, performance, and best practices while maintaining functionality:\n\n{code}"}
            ],
            max_tokens=1500
        )
        return response['choices'][0]['message']['content'].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error while communicating with OpenAI API: {e}")

def format_code_with_black(file_path):
    """Formats the given Python file using Black."""
    try:
        file_path = Path(file_path)  # Ensure file_path is a Path object
        if not file_path.exists():
            raise FileNotFoundError(f"File '{file_path}' does not exist.")
        format_file_in_place(
            src=file_path,
            fast=False,
            mode=FileMode(),
            write_back=WriteBack.YES
        )
    except Exception as e:
        raise RuntimeError(f"Error while formatting code with Black: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Refactor Assistant helps refactor Python scripts.")
    parser.add_argument("--file", required=True, help="Path to the Python file to refactor.")
    parser.add_argument("--write-back", action="store_true", help="Write the refactored code back to the file.")
    parser.add_argument("--api-key", required=True, help="OpenAI API key for generating refactored code.")

    args = parser.parse_args()
    console = Console()

    file_path = args.file
    if not os.path.isfile(file_path):
        console.print(f"[red]Error: File '{file_path}' does not exist.[/red]")
        return

    try:
        with open(file_path, "r") as file:
            original_code = file.read()

        console.print("[blue]Refactoring code using AI...[/blue]")
        refactored_code = refactor_code_with_ai(args.api_key, original_code)

        console.print("[green]Refactored Code:[/green]")
        syntax = Syntax(refactored_code, "python", theme="monokai", line_numbers=True)
        console.print(syntax)

        if args.write_back:
            with open(file_path, "w") as file:
                file.write(refactored_code)
            format_code_with_black(file_path)
            console.print(f"[green]Refactored code has been written back to '{file_path}' and formatted with Black.[/green]")

    except RuntimeError as e:
        console.print(f"[red]{e}[/red]")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}[/red]")

if __name__ == "__main__":
    main()
