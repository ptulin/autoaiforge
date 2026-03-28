import argparse
import requests
from rich.console import Console
from rich.table import Table

def perform_code_review(file_path, api_key):
    """
    Perform code review using Claude AI API.

    Args:
        file_path (str): Path to the Python file to review.
        api_key (str): Claude API key.

    Returns:
        dict: Review feedback from Claude AI.
    """
    try:
        # Read the file content
        with open(file_path, 'r') as file:
            code_content = file.read()

        # API request payload
        payload = {
            "code": code_content
        }

        # API endpoint (replace with actual Claude endpoint)
        url = "https://api.claude.ai/code-review"

        # Send request to Claude API
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)

        # Handle response
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch review: {response.status_code} {response.text}"}

    except FileNotFoundError:
        return {"error": "File not found. Please provide a valid file path."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {str(e)}"}

def display_feedback(feedback):
    """
    Display code review feedback in a styled CLI report.

    Args:
        feedback (dict): Feedback from Claude AI.
    """
    console = Console()

    if "error" in feedback:
        console.print(f"[bold red]Error:[/bold red] {feedback['error']}")
        return

    table = Table(title="Claude Code Review Feedback")
    table.add_column("Issue", style="cyan", no_wrap=True)
    table.add_column("Suggestion", style="magenta")

    for issue in feedback.get("issues", []):
        table.add_row(issue.get("issue", "Unknown issue"), issue.get("suggestion", "No suggestion"))

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="Claude Code Review Assistant")
    parser.add_argument("--file", required=True, help="Path to the Python file to review.")
    parser.add_argument("--api-key", required=True, help="Claude API key.")

    args = parser.parse_args()

    feedback = perform_code_review(args.file, args.api_key)
    display_feedback(feedback)

if __name__ == "__main__":
    main()
