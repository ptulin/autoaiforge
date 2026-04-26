import os
import sys
import subprocess
import yaml
import argparse
from openai import ChatCompletion

def get_staged_files():
    """Get a list of staged Python files."""
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        files = result.stdout.splitlines()
        return [f for f in files if f.endswith(".py")]
    except subprocess.CalledProcessError as e:
        print(f"Error while fetching staged files: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def analyze_code_with_claude(file_content, api_key):
    """Send the file content to Claude AI for analysis."""
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code review assistant."},
                {"role": "user", "content": f"Please review the following Python code for style, bugs, and optimization opportunities:\n\n{file_content}"}
            ],
            api_key=api_key
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error analyzing code with Claude: {str(e)}"

def run_linter(api_key):
    """Main function to run the linter on staged Python files."""
    staged_files = get_staged_files()

    if not staged_files:
        print("No staged Python files to analyze.")
        return

    for file_path in staged_files:
        print(f"Analyzing {file_path}...")
        try:
            with open(file_path, "r") as f:
                file_content = f.read()

            if not file_content.strip():
                print(f"{file_path} is empty. Skipping.")
                continue

            feedback = analyze_code_with_claude(file_content, api_key)
            print(f"Feedback for {file_path}:\n{feedback}\n")

        except FileNotFoundError:
            print(f"File {file_path} not found. Skipping.", file=sys.stderr)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}", file=sys.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Claude CI Linter")
    parser.add_argument(
        "--api-key",
        required=True,
        help="Your Claude API key for analyzing code."
    )

    args = parser.parse_args()
    run_linter(args.api_key)
