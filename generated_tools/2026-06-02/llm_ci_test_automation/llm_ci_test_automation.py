import os
import requests
import openai
from typing import List, Dict

def fetch_pr_diff(repo_url: str, pr_id: int, token: str) -> str:
    """
    Fetch the diff of a pull request from a GitHub repository.

    Args:
        repo_url (str): The GitHub repository URL.
        pr_id (int): The pull request ID.
        token (str): GitHub personal access token for authentication.

    Returns:
        str: The diff of the pull request.

    Raises:
        ValueError: If the response from GitHub is not successful.
    """
    headers = {"Authorization": f"token {token}"}
    api_url = f"https://api.github.com/repos/{'/'.join(repo_url.split('/')[-2:])}/pulls/{pr_id}"
    response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch PR diff: {response.status_code}, {response.text}")

    pr_data = response.json()
    diff_url = pr_data.get("diff_url")

    if not diff_url:
        raise ValueError("No diff URL found in the pull request data.")

    diff_response = requests.get(diff_url, headers=headers)

    if diff_response.status_code != 200:
        raise ValueError(f"Failed to fetch diff content: {diff_response.status_code}, {diff_response.text}")

    return diff_response.text

def generate_test_cases(repo_url: str, pr_id: int, token: str, openai_api_key: str) -> List[Dict[str, str]]:
    """
    Generate test cases for a pull request using OpenAI's LLM.

    Args:
        repo_url (str): The GitHub repository URL.
        pr_id (int): The pull request ID.
        token (str): GitHub personal access token for authentication.
        openai_api_key (str): OpenAI API key for generating test cases.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing test case information.
    """
    openai.api_key = openai_api_key

    try:
        diff = fetch_pr_diff(repo_url, pr_id, token)
    except ValueError as e:
        raise RuntimeError(f"Error fetching PR diff: {e}")

    prompt = (
        "Given the following code diff, generate Python test cases in JSON format. "
        "Each test case should include a 'name' and 'code' field. The 'code' field should "
        "contain the Python code for the test case.\n\n"
        f"Diff:\n{diff}\n\nTest cases:"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.3
        )
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error generating test cases: {e}")

    test_cases = response.choices[0].text.strip()

    try:
        return eval(test_cases)  # Convert the string output to a Python list
    except (SyntaxError, ValueError):
        raise RuntimeError("Failed to parse generated test cases.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="LLM-Integrated CI Test Automation Library"
    )
    parser.add_argument("--repo_url", required=True, help="GitHub repository URL")
    parser.add_argument("--pr_id", type=int, required=True, help="Pull request ID")
    parser.add_argument("--github_token", required=True, help="GitHub personal access token")
    parser.add_argument("--openai_api_key", required=True, help="OpenAI API key")

    args = parser.parse_args()

    try:
        test_cases = generate_test_cases(
            repo_url=args.repo_url,
            pr_id=args.pr_id,
            token=args.github_token,
            openai_api_key=args.openai_api_key
        )
        print("Generated Test Cases:")
        for test_case in test_cases:
            print(test_case)
    except Exception as e:
        print(f"Error: {e}")