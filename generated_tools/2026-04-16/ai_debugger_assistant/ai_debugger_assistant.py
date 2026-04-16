import argparse
import os
import openai
from rich.console import Console
from rich.text import Text

def analyze_traceback(file_path, error_log=None):
    """
    Analyzes the traceback and provides AI-powered suggestions for fixing errors.

    Args:
        file_path (str): Path to the Python script file.
        error_log (str, optional): Error log or traceback.

    Returns:
        str: AI-generated suggestions and explanations.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        script_content = file.read()

    prompt = f"""
    You are an AI debugging assistant. Analyze the following Python script and error traceback.
    Provide detailed explanations of the issues and suggest fixes.

    Script:
    {script_content}

    Error Traceback:
    {error_log or "No traceback provided."}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful debugging assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"An error occurred while communicating with the AI: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="AI Debugger Assistant")
    parser.add_argument('--file', required=True, help="Path to the Python script file.")
    parser.add_argument('--error-log', help="Optional error log or traceback.")
    args = parser.parse_args()

    console = Console()

    try:
        suggestions = analyze_traceback(args.file, args.error_log)
        console.print(Text(suggestions, style="bold green"))
    except FileNotFoundError as e:
        console.print(Text(str(e), style="bold red"))
    except Exception as e:
        console.print(Text(f"An unexpected error occurred: {str(e)}", style="bold red"))

if __name__ == "__main__":
    main()
