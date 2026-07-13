import openai
import requests
import argparse
import json

def analyze_pr(pr_id, repo, api_key):
    """
    Analyze a pull request for potential bugs and generate suggestions.

    Args:
        pr_id (str): Pull request ID.
        repo (str): Repository name in the format 'user/repo'.
        api_key (str): OpenAI API key.

    Returns:
        dict: JSON object containing AI-generated bug reports and suggested fixes.
    """
    if not pr_id or not repo or not api_key:
        raise ValueError("pr_id, repo, and api_key are required parameters.")

    # Fetch pull request diff
    try:
        url = f"https://api.github.com/repos/{repo}/pulls/{pr_id}"
        headers = {"Authorization": f"token {api_key}"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch pull request: {str(e)}"}

    pr_data = response.json()
    diff_url = pr_data.get("diff_url")
    if not diff_url:
        return {"error": "Diff URL not found in pull request data."}

    try:
        diff_response = requests.get(diff_url, headers=headers)
        diff_response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"error": f"Failed to fetch diff: {str(e)}"}

    diff_content = diff_response.text

    # Call OpenAI API for analysis
    try:
        openai.api_key = api_key
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following pull request diff for potential bugs and suggest fixes:\n{diff_content}",
            max_tokens=1000
        )
        suggestions = completion.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return {"error": f"Failed to analyze diff with OpenAI: {str(e)}"}

    return {
        "pr_id": pr_id,
        "repo": repo,
        "suggestions": suggestions
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pull Request AI Debugger")
    parser.add_argument("--pr_id", required=True, help="Pull request ID")
    parser.add_argument("--repo", required=True, help="Repository name in the format 'user/repo'")
    parser.add_argument("--api_key", required=True, help="OpenAI API key")

    args = parser.parse_args()

    result = analyze_pr(args.pr_id, args.repo, args.api_key)
    print(json.dumps(result, indent=2))