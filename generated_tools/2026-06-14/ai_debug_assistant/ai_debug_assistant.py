import argparse
import openai
from rich.console import Console
from rich.panel import Panel
import os

def analyze_error_message(error_message):
    """
    Analyze the given Python error message using OpenAI's GPT model
    and return debugging suggestions.

    Args:
        error_message (str): The Python error message to analyze.

    Returns:
        str: Debugging suggestions and potential fixes.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            return "OPENAI_API_KEY environment variable is not set."

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                f"You are an expert Python debugging assistant. Analyze the following error message and provide a detailed explanation, possible causes, and potential fixes with code snippets if applicable:\n\n"
                f"Error Message: {error_message}\n"
            ),
            max_tokens=300,
            temperature=0.7
        )

        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred while processing the error message: {str(e)}"

def main():
    parser = argparse.ArgumentParser(
        description="AI Debug Assistant: Analyze Python error messages and get debugging suggestions."
    )
    parser.add_argument(
        "--error",
        type=str,
        help="The Python error message to analyze.",
        required=False
    )
    parser.add_argument(
        "--logfile",
        type=str,
        help="Path to a log file containing the Python error message.",
        required=False
    )

    args = parser.parse_args()

    if not args.error and not args.logfile:
        print("Error: You must provide either --error or --logfile.")
        return

    if args.logfile:
        try:
            with open(args.logfile, "r") as file:
                error_message = file.read().strip()
        except FileNotFoundError:
            print(f"Error: The file '{args.logfile}' was not found.")
            return
        except Exception as e:
            print(f"Error: Unable to read the file. {str(e)}")
            return
    else:
        error_message = args.error

    if not error_message:
        print("Error: The provided error message is empty.")
        return

    console = Console()
    console.print(Panel.fit("[bold blue]Analyzing error message...[/bold blue]"))
    suggestions = analyze_error_message(error_message)
    console.print(Panel(suggestions, title="[green]Debugging Suggestions[/green]", expand=False))

if __name__ == "__main__":
    main()