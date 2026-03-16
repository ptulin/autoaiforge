import argparse
import os
import openai
from rich.console import Console
from rich.table import Table

def analyze_error_log(api_key, error_log, code_path):
    """
    Analyze the error log and provide debugging suggestions using OpenAI API.

    Args:
        api_key (str): OpenAI API key.
        error_log (str): The error log content.
        code_path (str): Path to the code files for context.

    Returns:
        str: AI-generated debugging suggestions.
    """
    openai.api_key = api_key

    # Prepare the prompt for the AI model
    prompt = f"""
    You are an expert software engineer. Analyze the following error log and provide debugging suggestions.
    Error Log:
    {error_log}

    Additionally, consider the context of the code in the following directory:
    {code_path}

    Provide step-by-step debugging suggestions.
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI API: {e}"

def read_file(file_path):
    """
    Read the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="AI Debug Assist: Analyze error logs and provide debugging suggestions.")
    parser.add_argument('--api-key', type=str, required=True, help="Your OpenAI API key.")
    parser.add_argument('--error-log', type=str, required=True, help="Path to the error log file.")
    parser.add_argument('--code-path', type=str, required=True, help="Path to the code directory for context.")

    args = parser.parse_args()

    console = Console()

    try:
        error_log_content = read_file(args.error_log)
        suggestions = analyze_error_log(args.api_key, error_log_content, args.code_path)

        table = Table(title="AI Debugging Suggestions")
        table.add_column("Suggestions", style="cyan")
        table.add_row(suggestions)

        console.print(table)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
    except Exception as e:
        console.print(f"[red]Unexpected error:[/red] {e}")

if __name__ == "__main__":
    main()