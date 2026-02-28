import os
import ast
import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

def review_code(file_path, api_key):
    """
    Analyze a Python file for potential issues using OpenAI API.

    Args:
        file_path (str): Path to the Python file to review.
        api_key (str): OpenAI API key.

    Returns:
        str: AI-generated review report.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        code = f.read()

    try:
        ast.parse(code)
    except SyntaxError as e:
        return f"Syntax Error in file {file_path}: {e}"

    openai.api_key = api_key

    prompt = (
        "You are an expert Python developer. Review the following code for bugs, inefficiencies, and style issues. "
        "Provide actionable feedback and suggestions for improvement:\n\n" + code
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI API: {e}"

def review_directory(directory_path, api_key):
    """
    Analyze all Python files in a directory.

    Args:
        directory_path (str): Path to the directory containing Python files.
        api_key (str): OpenAI API key.

    Returns:
        dict: Dictionary mapping file names to review reports.
    """
    if not os.path.isdir(directory_path):
        raise FileNotFoundError(f"Directory not found: {directory_path}")

    reports = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    reports[file] = review_code(file_path, api_key)
                except FileNotFoundError:
                    reports[file] = f"File not found: {file_path}"

    return reports

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Smart Code Review Bot")
    parser.add_argument("path", help="Path to a Python file or directory")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")

    args = parser.parse_args()

    if os.path.isfile(args.path):
        print(review_code(args.path, args.api_key))
    elif os.path.isdir(args.path):
        reports = review_directory(args.path, args.api_key)
        for file, report in reports.items():
            print(f"\nReview for {file}:\n")
            print(highlight(report, PythonLexer(), TerminalFormatter()))
    else:
        print("Invalid path. Please provide a valid file or directory.")