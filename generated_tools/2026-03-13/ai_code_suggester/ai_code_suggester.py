import argparse
import os
import openai
from rich.console import Console
from rich.syntax import Syntax
from rich.prompt import Prompt

# Initialize the console for rich output
console = Console()

def get_code_suggestions(api_key, file_content, model="claude-v1", max_tokens=150):
    """
    Fetch code suggestions from Claude AI based on the given file content.

    Args:
        api_key (str): API key for OpenAI.
        file_content (str): Content of the Python file to analyze.
        model (str): Claude AI model to use.
        max_tokens (int): Maximum tokens for the response.

    Returns:
        str: Suggested code snippet.
    """
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine=model,
            prompt=f"Provide suggestions to complete the following Python code:\n{file_content}\n\nSuggestions:",
            max_tokens=max_tokens,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        console.print(f"[red]Error fetching suggestions: {e}[/red]")
        return ""

def analyze_file(file_path, api_key, model="claude-v1", max_tokens=150, inline=False):
    """
    Analyze a Python file and provide code suggestions.

    Args:
        file_path (str): Path to the Python file to analyze.
        api_key (str): API key for OpenAI.
        model (str): Claude AI model to use.
        max_tokens (int): Maximum tokens for the response.
        inline (bool): Whether to add suggestions inline as comments.

    Returns:
        None
    """
    if not os.path.exists(file_path):
        console.print(f"[red]Error: File '{file_path}' does not exist.[/red]")
        return

    try:
        with open(file_path, "r") as file:
            file_content = file.read()
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        return

    suggestions = get_code_suggestions(api_key, file_content, model, max_tokens)

    if not suggestions:
        console.print("[yellow]No suggestions were generated.[/yellow]")
        return

    if inline:
        try:
            with open(file_path, "a") as file:
                file.write(f"\n# Suggestions from Claude AI:\n# " + suggestions.replace("\n", "\n# "))
            console.print(f"[green]Suggestions added inline to '{file_path}'.[/green]")
        except Exception as e:
            console.print(f"[red]Error writing to file: {e}[/red]")
    else:
        console.print("[cyan]Code Suggestions:[/cyan]")
        console.print(Syntax(suggestions, "python"))

def main():
    parser = argparse.ArgumentParser(description="AI Code Suggester: Get real-time code suggestions for Python files.")
    parser.add_argument("--file", required=True, help="Path to the Python file to analyze.")
    parser.add_argument("--api-key", required=True, help="OpenAI API key.")
    parser.add_argument("--model", default="claude-v1", help="Claude AI model to use (default: claude-v1).")
    parser.add_argument("--max-tokens", type=int, default=150, help="Maximum tokens for the AI response (default: 150).")
    parser.add_argument("--inline", action="store_true", help="Add suggestions inline as comments in the file.")

    args = parser.parse_args()

    analyze_file(
        file_path=args.file,
        api_key=args.api_key,
        model=args.model,
        max_tokens=args.max_tokens,
        inline=args.inline
    )

if __name__ == "__main__":
    main()
