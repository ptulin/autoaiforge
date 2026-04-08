import os
import argparse
from openai import ChatCompletion
from rich.console import Console
from rich.table import Table

# Initialize the console for rich output
console = Console()

def analyze_code(file_content, review_type):
    """
    Analyze the provided code using OpenAI's API and return suggestions.

    Args:
        file_content (str): The content of the code file to analyze.
        review_type (str): The type of review to perform (e.g., performance, readability).

    Returns:
        dict: A dictionary containing issues and suggestions.
    """
    try:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            return {"success": False, "error": "OPENAI_API_KEY environment variable is not set."}

        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are a code review assistant. Provide detailed suggestions for improvement."
                },
                {
                    "role": "user",
                    "content": f"Review this code for {review_type} issues:\n\n{file_content}"
                }
            ]
        )

        suggestions = response['choices'][0]['message']['content']
        return {"success": True, "suggestions": suggestions}

    except Exception as e:
        return {"success": False, "error": str(e)}

def process_path(path, review_type):
    """
    Process the given file or directory path for code review.

    Args:
        path (str): Path to the file or directory.
        review_type (str): The type of review to perform.

    Returns:
        list: A list of dictionaries containing file names and their review results.
    """
    results = []

    if os.path.isfile(path):
        try:
            with open(path, 'r') as file:
                file_content = file.read()
            result = analyze_code(file_content, review_type)
            results.append({"file": path, "result": result})
        except Exception as e:
            results.append({"file": path, "result": {"success": False, "error": str(e)}})

    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            file_content = f.read()
                        result = analyze_code(file_content, review_type)
                        results.append({"file": file_path, "result": result})
                    except Exception as e:
                        results.append({"file": file_path, "result": {"success": False, "error": str(e)}})

    else:
        console.print(f"[red]Error: The path '{path}' is not valid.[/red]")

    return results

def generate_report(results, output_file=None):
    """
    Generate a report of the code review results.

    Args:
        results (list): List of code review results.
        output_file (str, optional): File path to save the report. Defaults to None.
    """
    table = Table(title="AI Code Review Report")
    table.add_column("File", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Details", style="white")

    for result in results:
        file = result['file']
        if result['result']['success']:
            table.add_row(file, "Success", result['result']['suggestions'])
        else:
            table.add_row(file, "Error", result['result']['error'])

    console.print(table)

    if output_file:
        with open(output_file, 'w') as f:
            for result in results:
                f.write(f"File: {result['file']}\n")
                if result['result']['success']:
                    f.write(f"Suggestions:\n{result['result']['suggestions']}\n\n")
                else:
                    f.write(f"Error: {result['result']['error']}\n\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Code Review Bot")
    parser.add_argument("path", help="Path to the file or directory to review")
    parser.add_argument("review_type", help="Type of review to perform (e.g., readability, performance)")
    parser.add_argument("--output", help="File path to save the report", default=None)

    args = parser.parse_args()

    results = process_path(args.path, args.review_type)
    generate_report(results, args.output)
