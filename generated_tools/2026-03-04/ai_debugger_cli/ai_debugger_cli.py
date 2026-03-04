import sys
import json
import click
from rich.console import Console
from rich.panel import Panel
from openai import ChatCompletion, OpenAIError

# Initialize rich console for pretty printing
console = Console()

@click.command()
@click.option('--file', type=click.Path(exists=True), help='Path to the file containing the error log.')
def main(file):
    """AI Debugger CLI: Analyze Python stack traces and errors with AI."""
    if not file and sys.stdin.isatty():
        console.print("[bold red]Error:[/] No input provided. Use --file or pipe error logs to stdin.")
        sys.exit(1)

    # Read input from file or stdin
    try:
        if file:
            with open(file, 'r') as f:
                error_log = f.read()
        else:
            error_log = sys.stdin.read()

        if not error_log.strip():
            console.print("[bold red]Error:[/] Empty input provided.")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error:[/] Unable to read input: {e}")
        sys.exit(1)

    # Process the error log with AI
    try:
        response = analyze_with_ai(error_log)
        console.print(Panel(response, title="AI Debugger Response", expand=False))
    except OpenAIError as e:
        console.print(f"[bold red]Error:[/] Failed to communicate with AI: {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/] {e}")
        sys.exit(1)

def analyze_with_ai(error_log):
    """Send the error log to Claude AI for analysis and return the response."""
    # Replace with your OpenAI API key
    api_key = "your_openai_api_key"

    if not api_key:
        raise ValueError("OpenAI API key is not set.")

    ChatCompletion.api_key = api_key

    messages = [
        {"role": "system", "content": "You are an expert Python debugger."},
        {"role": "user", "content": f"Here is a Python error log: {error_log}"}
    ]

    response = ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )

    return response['choices'][0]['message']['content']

if __name__ == "__main__":
    main()