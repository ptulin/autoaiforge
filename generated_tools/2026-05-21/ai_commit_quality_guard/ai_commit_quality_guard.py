import os
import sys
import subprocess
import yaml
import argparse
from openai import ChatCompletion

def load_config(config_path):
    """Load configuration from a YAML file."""
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, 'r') as file:
            return yaml.safe_load(file) or {}
    except yaml.YAMLError as e:
        print(f"Error loading configuration file: {e}", file=sys.stderr)
        return {}

def get_staged_files():
    """Retrieve a list of staged Python files."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        result.check_returncode()
        files = result.stdout.splitlines()
        return [f for f in files if f.endswith('.py')]
    except subprocess.CalledProcessError as e:
        print(f"Error retrieving staged files: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def review_code(file_content, openai_api_key):
    """Use OpenAI's API to review the code for quality issues."""
    try:
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code quality reviewer."},
                {"role": "user", "content": f"Please review the following Python code for bugs, stylistic issues, and adherence to best practices:\n\n{file_content}"}
            ],
            api_key=openai_api_key
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error during code review: {e}"

def main():
    parser = argparse.ArgumentParser(description="AI Commit Quality Guard")
    parser.add_argument('--config', type=str, default='.ai_commit_quality_guard.yaml', help="Path to configuration file")
    args = parser.parse_args()

    config = load_config(args.config)
    openai_api_key = os.getenv('OPENAI_API_KEY')

    if not openai_api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    staged_files = get_staged_files()

    if not staged_files:
        print("No staged Python files to review.")
        sys.exit(0)

    block_commit = False

    for file_path in staged_files:
        print(f"Reviewing {file_path}...")
        try:
            with open(file_path, 'r') as file:
                file_content = file.read()
            review_result = review_code(file_content, openai_api_key)
            print(f"Review for {file_path}:")
            print(review_result)

            if 'issue' in review_result.lower():
                block_commit = True
        except FileNotFoundError:
            print(f"Error: File {file_path} not found.", file=sys.stderr)
            block_commit = True

    if block_commit:
        print("Commit blocked due to issues found in the code.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
