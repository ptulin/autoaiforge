import argparse
import os
import openai
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel

def analyze_code(file_path, api_key):
    """
    Analyze the Python code in the given file using OpenAI's API.

    Args:
        file_path (str): Path to the Python file to analyze.
        api_key (str): OpenAI API key.

    Returns:
        str: A string containing the analysis result.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        code = file.read()

    if not code.strip():
        raise ValueError("The provided file is empty.")

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python debugging assistant."},
                {"role": "user", "content": f"Please analyze the following Python code and provide error explanations and fixes:\n\n{code}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"OpenAI API error: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Claude Debug CLI: Analyze and debug Python scripts using OpenAI's GPT-4."
    )
    parser.add_argument('--file', required=True, help="Path to the Python file to analyze.")
    parser.add_argument('--api-key', required=True, help="Your OpenAI API key.")
    parser.add_argument('--output', help="Optional output file to save the debugged code.")

    args = parser.parse_args()

    console = Console()

    try:
        console.print("[bold green]Analyzing the Python script...[/bold green]")
        analysis_result = analyze_code(args.file, args.api_key)

        console.print(Panel("[bold yellow]Analysis Result:[/bold yellow]", expand=False))
        syntax = Syntax(analysis_result, "python", theme="monokai", line_numbers=True)
        console.print(syntax)

        if args.output:
            with open(args.output, 'w') as output_file:
                output_file.write(analysis_result)
            console.print(f"[bold green]Analysis saved to {args.output}[/bold green]")

    except FileNotFoundError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
    except RuntimeError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
