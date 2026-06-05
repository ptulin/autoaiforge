import argparse
import os
import sys
from git import Repo, GitCommandError
from openai import ChatCompletion
from colorama import Fore, Style

def analyze_commit_message(message, api_key):
    """Analyze a commit message using OpenAI's API."""
    try:
        import openai
        openai.api_key = api_key
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an assistant that reviews Git commit messages for clarity, conciseness, and relevance."
                },
                {
                    "role": "user",
                    "content": f"Review this commit message: {message}"
                }
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error analyzing commit message: {e}"

def get_commit_messages(repo_path, commit_hash=None):
    """Retrieve commit messages from a Git repository."""
    try:
        repo = Repo(repo_path)
        if commit_hash:
            commit = repo.commit(commit_hash)
            return [commit.message.strip()]
        else:
            return [commit.message.strip() for commit in repo.iter_commits()]
    except GitCommandError as e:
        sys.exit(f"Git error: {e}")
    except Exception as e:
        sys.exit(f"Error accessing repository: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="AI-Powered Commit Message Linter"
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Path to the Git repository"
    )
    parser.add_argument(
        "--commit",
        type=str,
        help="Specific commit hash to analyze (optional)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        required=True,
        help="OpenAI API key"
    )

    args = parser.parse_args()

    if not os.path.exists(args.repo):
        sys.exit("Error: The specified repository path does not exist.")

    commit_messages = get_commit_messages(args.repo, args.commit)

    for i, message in enumerate(commit_messages):
        print(f"{Fore.CYAN}Commit {i + 1}:{Style.RESET_ALL} {message}\n")
        print(f"{Fore.YELLOW}Analysis:{Style.RESET_ALL}")
        analysis = analyze_commit_message(message, args.api_key)
        print(f"{Fore.GREEN}{analysis}{Style.RESET_ALL}\n")

if __name__ == "__main__":
    main()