import argparse
import requests
import os

def get_code_suggestion(api_key, description, language):
    """
    Fetches a code suggestion from an AI API based on the provided description and language.

    Args:
        api_key (str): The API key for the AI service.
        description (str): The function description or partial code snippet.
        language (str): The programming language for the suggestion.

    Returns:
        str: The suggested code snippet.

    Raises:
        ValueError: If the API key is missing.
        requests.RequestException: If there is an issue with the API request.
    """
    if not api_key:
        raise ValueError("API key is required to fetch code suggestions.")

    url = "https://api.openai.com/v1/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "text-davinci-003",
        "prompt": f"Write a {language} function: {description}",
        "max_tokens": 150
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("choices", [{}])[0].get("text", "No suggestion available.").strip()
    except requests.RequestException as e:
        raise requests.RequestException(f"Failed to fetch code suggestion: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Code Suggestion CLI")
    parser.add_argument("--description", required=True, help="Function description or partial code snippet.")
    parser.add_argument("--language", required=True, help="Programming language (e.g., python, javascript, etc.).")
    parser.add_argument("--output", help="File to save the suggested code snippet.")
    args = parser.parse_args()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return

    try:
        suggestion = get_code_suggestion(api_key, args.description, args.language)
        if args.output:
            with open(args.output, "w") as file:
                file.write(suggestion)
            print(f"Code suggestion saved to {args.output}")
        else:
            print("Suggested Code:")
            print(suggestion)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()