import argparse
import os
from rich.console import Console
from rich.prompt import Prompt
import openai
import anthropic

def analyze_traceback_with_gpt(traceback: str, api_key: str) -> str:
    """Analyze the traceback using OpenAI's GPT model."""
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python debugging assistant."},
                {"role": "user", "content": f"Here is a Python traceback:\n{traceback}\nPlease analyze it and suggest fixes."}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error communicating with GPT API: {e}"

def analyze_traceback_with_claude(traceback: str, api_key: str) -> str:
    """Analyze the traceback using Anthropic's Claude model."""
    client = anthropic.Client(api_key)
    try:
        response = client.completion(
            prompt=f"\n\nHuman: Here is a Python traceback:\n{traceback}\nPlease analyze it and suggest fixes.\n\nAssistant:",
            model="claude-v1",
            max_tokens_to_sample=300
        )
        return response['completion']
    except Exception as e:
        return f"Error communicating with Claude API: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="GPT-Claude Debug Assistant: Analyze Python error tracebacks and suggest fixes."
    )
    parser.add_argument(
        '--error-log', '-e',
        type=str,
        help="Path to a file containing the Python error traceback."
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help="Enable interactive mode for back-and-forth clarification."
    )
    parser.add_argument(
        '--gpt-api-key',
        type=str,
        required=True,
        help="Your OpenAI API key."
    )
    parser.add_argument(
        '--claude-api-key',
        type=str,
        required=True,
        help="Your Anthropic Claude API key."
    )

    args = parser.parse_args()
    console = Console()

    if args.error_log:
        if not os.path.exists(args.error_log):
            console.print(f"[red]Error: File '{args.error_log}' does not exist.[/red]")
            return

        with open(args.error_log, 'r') as file:
            traceback = file.read()
    else:
        console.print("[yellow]No error log provided. Please paste the traceback below (end with an empty line):[/yellow]")
        traceback_lines = []
        while True:
            line = input()
            if not line.strip():
                break
            traceback_lines.append(line)
        traceback = "\n".join(traceback_lines)

    if not traceback.strip():
        console.print("[red]Error: No traceback provided.[/red]")
        return

    console.print("[blue]Analyzing traceback with GPT...[/blue]")
    gpt_response = analyze_traceback_with_gpt(traceback, args.gpt_api_key)
    console.print("[green]GPT Response:[/green]")
    console.print(gpt_response)

    console.print("[blue]Analyzing traceback with Claude...[/blue]")
    claude_response = analyze_traceback_with_claude(traceback, args.claude_api_key)
    console.print("[green]Claude Response:[/green]")
    console.print(claude_response)

    if args.interactive:
        while True:
            follow_up = Prompt.ask("[cyan]Enter a follow-up question or type 'exit' to quit[/cyan]")
            if follow_up.lower() == 'exit':
                break

            console.print("[blue]Asking GPT...[/blue]")
            gpt_follow_up = analyze_traceback_with_gpt(follow_up, args.gpt_api_key)
            console.print("[green]GPT Follow-Up Response:[/green]")
            console.print(gpt_follow_up)

            console.print("[blue]Asking Claude...[/blue]")
            claude_follow_up = analyze_traceback_with_claude(follow_up, args.claude_api_key)
            console.print("[green]Claude Follow-Up Response:[/green]")
            console.print(claude_follow_up)

if __name__ == "__main__":
    main()