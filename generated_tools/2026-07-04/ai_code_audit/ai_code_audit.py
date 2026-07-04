import os
import ast
import argparse
from typing import List, Tuple
from rich.console import Console
from rich.table import Table
import openai

# Set up the OpenAI API key (replace with your own key or set it via environment variable)
openai.api_key = os.getenv("OPENAI_API_KEY")

def analyze_code_with_openai(code: str) -> List[str]:
    """
    Analyze Python code using OpenAI's language model to detect inefficiencies,
    vulnerabilities, and provide suggestions.

    Args:
        code (str): The Python code to analyze.

    Returns:
        List[str]: A list of issues with severity and suggestions.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following Python code for inefficiencies, unused imports, and security vulnerabilities. Provide actionable fixes with explanations:\n\n{code}",
            max_tokens=500,
            temperature=0.2
        )
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["text"].strip().split("\n")
        else:
            return ["No issues found"]
    except Exception as e:
        return [f"Error analyzing code with OpenAI: {e}"]

def analyze_file(file_path: str) -> List[Tuple[str, str, str]]:
    """
    Analyze a single Python file for issues.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        List[Tuple[str, str, str]]: A list of issues with severity and suggestions.
    """
    try:
        with open(file_path, "r") as f:
            code = f.read()
        issues = analyze_code_with_openai(code)
        return [(file_path, "INFO", issue) for issue in issues]
    except Exception as e:
        return [(file_path, "ERROR", f"Failed to analyze file: {e}")]

def analyze_directory(directory_path: str) -> List[Tuple[str, str, str]]:
    """
    Analyze all Python files in a directory for issues.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        List[Tuple[str, str, str]]: A list of issues with severity and suggestions.
    """
    issues = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                issues.extend(analyze_file(file_path))
    return issues

def display_report(issues: List[Tuple[str, str, str]]) -> None:
    """
    Display the analysis report in the terminal.

    Args:
        issues (List[Tuple[str, str, str]]): A list of issues with severity and suggestions.
    """
    console = Console()
    table = Table(title="AI Code Audit Report")
    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Severity", style="magenta")
    table.add_column("Issue", style="white")

    for file, severity, issue in issues:
        table.add_row(file, severity, issue)

    console.print(table)

def main():
    parser = argparse.ArgumentParser(
        description="AI Code Audit: Analyze Python code for inefficiencies, vulnerabilities, and provide actionable fixes."
    )
    parser.add_argument(
        "--path", required=True, help="Path to a Python file or a directory containing Python files."
    )
    args = parser.parse_args()

    if not os.path.exists(args.path):
        print(f"Error: The path '{args.path}' does not exist.")
        return

    if os.path.isfile(args.path):
        issues = analyze_file(args.path)
    elif os.path.isdir(args.path):
        issues = analyze_directory(args.path)
    else:
        print(f"Error: The path '{args.path}' is neither a file nor a directory.")
        return

    display_report(issues)

if __name__ == "__main__":
    main()
