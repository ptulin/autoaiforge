import argparse
import requests
import openai
import os

def fetch_pr_diff(token, repo, pr_id):
    """Fetch the diff of a pull request from GitHub."""
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_id}"
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/vnd.github.v3.diff"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        raise ValueError(f"Failed to fetch PR diff: {response.status_code} {response.reason}")

def suggest_refactors(diff, openai_api_key):
    """Use OpenAI's API to suggest refactor opportunities based on the diff."""
    openai.api_key = openai_api_key

    prompt = (
        "You are a code review assistant. Analyze the following Git diff for code smells, "
        "design anti-patterns, and suggest refactor opportunities. Provide detailed suggestions "
        "in a markdown format:\n\n"
        f"{diff}"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to get suggestions from OpenAI: {e}")

def main():
    parser = argparse.ArgumentParser(description="GitHub PR Refactor Suggester")
    parser.add_argument("--token", required=True, help="GitHub personal access token")
    parser.add_argument("--repo", required=True, help="GitHub repository in the format 'owner/repo'")
    parser.add_argument("--pr", required=True, type=int, help="Pull request ID")
    parser.add_argument("--openai-key", required=True, help="OpenAI API key")
    parser.add_argument("--output", help="Output file to save suggestions in markdown format")

    args = parser.parse_args()

    try:
        diff = fetch_pr_diff(args.token, args.repo, args.pr)
        suggestions = suggest_refactors(diff, args.openai_key)

        if args.output:
            with open(args.output, "w") as f:
                f.write(suggestions)
            print(f"Suggestions saved to {args.output}")
        else:
            print(suggestions)

    except ValueError as ve:
        print(f"Error: {ve}")
    except RuntimeError as re:
        print(f"Error: {re}")

if __name__ == "__main__":
    main()