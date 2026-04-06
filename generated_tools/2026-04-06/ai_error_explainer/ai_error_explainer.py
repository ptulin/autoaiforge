import argparse
import sys
from rich.console import Console
from rich.table import Table
import openai

# Set up the console for rich output
console = Console()

def explain_error(api_key, error_message):
    """
    Sends the error message to OpenAI's API and retrieves an explanation and potential fixes.

    Args:
        api_key (str): OpenAI API key.
        error_message (str): The error message to explain.

    Returns:
        dict: A dictionary containing the explanation and suggestions.
    """
    if not error_message.strip():
        return {"error": "Error message is empty."}

    openai.api_key = api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for explaining Python errors."},
                {"role": "user", "content": f"Explain this Python error and suggest fixes: {error_message}"}
            ]
        )
        explanation = response['choices'][0]['message']['content']
        return {"explanation": explanation.strip()}
    except openai.error.OpenAIError as e:
        return {"error": f"Failed to retrieve explanation: {str(e)}"}


def main():
    parser = argparse.ArgumentParser(
        description="AI Error Explainer: Get AI-powered explanations and fixes for Python errors."
    )
    parser.add_argument(
        '--error', type=str, help="The error message to explain. If not provided, the tool will read from stdin."
    )
    parser.add_argument(
        '--api-key', type=str, required=True, help="Your OpenAI API key."
    )

    args = parser.parse_args()

    # Read error message from stdin if not provided as an argument
    if not args.error:
        if sys.stdin.isatty():
            console.print("[red]Error: No error message provided. Use --error or provide input via stdin.")
            sys.exit(1)
        error_message = sys.stdin.read().strip()
    else:
        error_message = args.error

    if not error_message:
        console.print("[red]Error: No error message provided.")
        sys.exit(1)

    result = explain_error(args.api_key, error_message)

    if "error" in result:
        console.print(f"[red]{result['error']}")
    else:
        explanation = result["explanation"]
        table = Table(title="AI Error Explanation")
        table.add_column("Error Message", style="bold red")
        table.add_column("Explanation", style="bold green")
        table.add_row(error_message, explanation)
        console.print(table)

if __name__ == "__main__":
    main()
