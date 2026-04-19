import argparse
import os
import openai
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table

# Initialize rich console for pretty printing
console = Console()

def get_claude_response(prompt, api_key):
    """
    Function to interact with Claude Code API via OpenAI.

    Args:
        prompt (str): The input prompt to send to the Claude Code API.
        api_key (str): OpenAI API key.

    Returns:
        str: Response from the Claude Code API.
    """
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        console.print(f"[red]Error communicating with Claude Code API: {e}[/red]")
        return None

def process_code(file_path, action, api_key):
    """
    Process the code file based on the specified action.

    Args:
        file_path (str): Path to the code file.
        action (str): Action to perform (suggest, debug, annotate).
        api_key (str): OpenAI API key.

    Returns:
        str: Processed code or explanation.
    """
    if not os.path.isfile(file_path):
        console.print(f"[red]Error: File '{file_path}' does not exist.[/red]")
        return None

    try:
        with open(file_path, 'r') as file:
            code = file.read()
    except Exception as e:
        console.print(f"[red]Error reading file '{file_path}': {e}[/red]")
        return None

    prompt = f"Perform the following action on the code: {action}\n\nCode:\n{code}"
    return get_claude_response(prompt, api_key)

def main():
    parser = argparse.ArgumentParser(
        description="Claude Code Assist: A CLI tool for code suggestions, debugging, and annotations using Claude Code API."
    )
    parser.add_argument('--file', type=str, required=True, help="Path to the code file.")
    parser.add_argument('--action', type=str, choices=['suggest', 'debug', 'annotate'], required=True,
                        help="Action to perform on the code: suggest, debug, or annotate.")
    parser.add_argument('--api_key', type=str, required=True, help="OpenAI API key for Claude Code API.")
    parser.add_argument('--output', type=str, help="Optional output file to save the result.")

    args = parser.parse_args()

    result = process_code(args.file, args.action, args.api_key)

    if result:
        if args.output:
            try:
                with open(args.output, 'w') as output_file:
                    output_file.write(result)
                console.print(f"[green]Result saved to {args.output}[/green]")
            except Exception as e:
                console.print(f"[red]Error writing to file '{args.output}': {e}[/red]")
        else:
            console.print("\n[bold green]Result:[/bold green]")
            syntax = Syntax(result, "python", theme="monokai", line_numbers=True)
            console.print(syntax)

if __name__ == "__main__":
    main()