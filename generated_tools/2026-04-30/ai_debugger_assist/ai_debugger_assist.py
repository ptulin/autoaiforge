import sys
import json
import argparse
from rich.console import Console
from rich.panel import Panel
from openai import ChatCompletion, OpenAIError

console = Console()

def main():
    """AI Debugger Assist: Analyze Python stack traces and provide debugging suggestions."""
    parser = argparse.ArgumentParser(description="AI Debugger Assist")
    parser.add_argument('--trace', '-t', type=str, help='Python stack trace as input.')
    args = parser.parse_args()

    if not args.trace:
        console.print("[bold red]Error:[/bold red] No stack trace provided. Use --trace to provide a stack trace.")
        sys.exit(1)

    try:
        console.print("[bold green]Analyzing stack trace...[/bold green]")
        response = analyze_stack_trace(args.trace)
        console.print(Panel(response, title="[bold blue]Debugging Suggestions[/bold blue]", expand=False))
    except OpenAIError as e:
        console.print(f"[bold red]Error communicating with AI service:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Unexpected error:[/bold red] {e}")

def analyze_stack_trace(trace):
    """Send the stack trace to OpenAI's API and return the response."""
    if not trace.strip():
        raise ValueError("Empty stack trace provided.")

    try:
        # Mocked API call for testing purposes
        # Replace `api_key` with your OpenAI API key in a real implementation
        api_key = "your_openai_api_key"
        ChatCompletion.api_key = api_key

        messages = [
            {"role": "system", "content": "You are an expert Python debugger."},
            {"role": "user", "content": f"Analyze this Python stack trace and suggest fixes:\n{trace}"}
        ]

        response = ChatCompletion.create(
            model="gpt-4.0",
            messages=messages
        )

        return response['choices'][0]['message']['content']
    except OpenAIError as e:
        raise OpenAIError(f"Failed to analyze stack trace: {e}")

if __name__ == "__main__":
    main()
