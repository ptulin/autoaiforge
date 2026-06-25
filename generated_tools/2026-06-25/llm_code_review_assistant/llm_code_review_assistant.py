import argparse
import json
import requests
import openai
import yaml
from urllib.parse import urlparse

def fetch_pr_files(repo_url, pr_id):
    """
    Fetch the list of files changed in a pull request.

    Args:
        repo_url (str): The URL of the repository.
        pr_id (int): The pull request ID.

    Returns:
        list: A list of file contents.
    """
    # Extracting the platform and repository details from the URL
    parsed_url = urlparse(repo_url)
    if 'github.com' in parsed_url.netloc:
        api_url = f"https://api.github.com/repos{parsed_url.path}/pulls/{pr_id}/files"
    elif 'gitlab.com' in parsed_url.netloc:
        api_url = f"https://gitlab.com/api/v4/projects/{parsed_url.path[1:].replace('/', '%2F')}/merge_requests/{pr_id}/changes"
    else:
        raise ValueError("Unsupported repository platform. Only GitHub and GitLab are supported.")

    try:
        response = requests.get(api_url)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch pull request files: {e}")

    if 'github.com' in parsed_url.netloc:
        return [file['patch'] for file in response.json()]
    elif 'gitlab.com' in parsed_url.netloc:
        return [change['diff'] for change in response.json()['changes']]

def analyze_code_with_llm(file_contents, openai_api_key):
    """
    Analyze code using OpenAI's LLM.

    Args:
        file_contents (list): List of file content strings.
        openai_api_key (str): OpenAI API key.

    Returns:
        dict: Code review suggestions.
    """
    openai.api_key = openai_api_key

    suggestions = {}
    for idx, content in enumerate(file_contents):
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=(
                    "You are a code review assistant. Analyze the following code for potential bugs, "
                    "coding standards violations, and optimization suggestions. Provide actionable feedback:\n\n"
                    f"{content}"
                ),
                max_tokens=500
            )
            suggestions[f"file_{idx + 1}"] = response.choices[0].text.strip()
        except openai.error.OpenAIError as e:
            suggestions[f"file_{idx + 1}"] = f"Error analyzing file: {e}"

    return suggestions

def main():
    parser = argparse.ArgumentParser(description="LLM Code Review Assistant")
    parser.add_argument("--repo", required=True, help="Repository URL (GitHub or GitLab)")
    parser.add_argument("--pr", required=True, type=int, help="Pull Request ID")
    parser.add_argument("--output", help="Output file to save the review suggestions (JSON format)")
    parser.add_argument("--api-key", required=True, help="OpenAI API key")

    args = parser.parse_args()

    try:
        file_contents = fetch_pr_files(args.repo, args.pr)
        if not file_contents:
            print("No files found in the pull request.")
            return

        suggestions = analyze_code_with_llm(file_contents, args.api_key)

        if args.output:
            with open(args.output, "w") as f:
                json.dump(suggestions, f, indent=4)
            print(f"Code review suggestions saved to {args.output}")
        else:
            print(json.dumps(suggestions, indent=4))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()