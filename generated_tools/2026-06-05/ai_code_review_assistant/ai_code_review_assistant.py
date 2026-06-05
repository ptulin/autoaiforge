import os
import argparse
import openai
from pygments import highlight
from pygments.lexers import get_lexer_for_filename
from pygments.formatters import TerminalFormatter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

def analyze_code_with_ai(file_content, file_name):
    """Send the code to OpenAI API for analysis."""
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following code and provide feedback on errors, antipatterns, and style violations. File: {file_name}\n\n{file_content}",
            max_tokens=500,
            temperature=0.5
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error analyzing code: {e}"

def process_file(file_path):
    """Read the file and analyze its content."""
    if not os.path.isfile(file_path):
        return f"Error: {file_path} is not a valid file.", None

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        feedback = analyze_code_with_ai(content, file_path)
        lexer = get_lexer_for_filename(file_path, content)
        highlighted_code = highlight(content, lexer, TerminalFormatter())
        return feedback, highlighted_code
    except Exception as e:
        return f"Error reading file {file_path}: {e}", None

def analyze_directory(directory_path):
    """Analyze all code files in a directory."""
    if not os.path.isdir(directory_path):
        return [(f"Error: {directory_path} is not a valid directory.", None, None)]

    results = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            feedback, highlighted_code = process_file(file_path)
            results.append((file_path, feedback, highlighted_code))
    return results

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Assistant")
    parser.add_argument('--file', type=str, help="Path to a code file")
    parser.add_argument('--directory', type=str, help="Path to a directory containing code files")
    args = parser.parse_args()

    console = Console()

    if args.file:
        feedback, highlighted_code = process_file(args.file)
        if highlighted_code:
            console.print(Panel(Text(highlighted_code, style="bold"), title="Code Snippet"))
        console.print(Panel(feedback, title="AI Feedback"))

    elif args.directory:
        results = analyze_directory(args.directory)
        for file_path, feedback, highlighted_code in results:
            if feedback.startswith("Error"):
                console.print(Panel(feedback, style="bold red"))
            else:
                console.print(Panel(f"File: {file_path}", style="bold green"))
                if highlighted_code:
                    console.print(Panel(Text(highlighted_code, style="bold"), title="Code Snippet"))
                console.print(Panel(feedback, title="AI Feedback"))

    else:
        console.print("[bold red]Error: Please provide a file or directory to analyze.[/bold red]")

if __name__ == "__main__":
    main()
