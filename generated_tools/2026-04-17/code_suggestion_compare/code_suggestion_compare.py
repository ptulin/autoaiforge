import requests
import difflib
import black
import json
from typing import List, Dict

def fetch_code_suggestion(api_key: str, prompt: str) -> str:
    """
    Fetches a code suggestion from an AI model API.

    Args:
        api_key (str): API key for the model.
        prompt (str): The prompt to send to the model.

    Returns:
        str: The code suggestion returned by the model.
    """
    try:
        response = requests.post(
            "https://api.example.com/generate",  # Replace with actual API endpoint
            headers={"Authorization": f"Bearer {api_key}"},
            json={"prompt": prompt},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("code", "")
    except requests.exceptions.RequestException as e:
        return f"Error fetching suggestion: {e}"

def compare_suggestions(api_keys: List[str], prompt: str) -> Dict:
    """
    Compares code suggestions from multiple AI models.

    Args:
        api_keys (List[str]): List of API keys for the models.
        prompt (str): The prompt to send to the models.

    Returns:
        Dict: A dictionary containing the suggestions and their differences.
    """
    suggestions = {}

    for i, api_key in enumerate(api_keys):
        suggestion = fetch_code_suggestion(api_key, prompt)
        suggestions[f"model_{i+1}"] = suggestion

    diffs = {}
    model_keys = list(suggestions.keys())

    for i in range(len(model_keys)):
        for j in range(i + 1, len(model_keys)):
            model_a = model_keys[i]
            model_b = model_keys[j]
            diff = list(difflib.unified_diff(
                suggestions[model_a].splitlines(),
                suggestions[model_b].splitlines(),
                lineterm="",
                fromfile=model_a,
                tofile=model_b
            ))
            diffs[f"{model_a}_vs_{model_b}"] = "\n".join(diff)

    return {
        "suggestions": suggestions,
        "diffs": diffs
    }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Code Suggestion Comparator")
    parser.add_argument("--api_keys", nargs='+', required=True, help="List of API keys for the models.")
    parser.add_argument("--prompt", required=True, help="The prompt to send to the models.")
    parser.add_argument("--output", choices=["json", "diff"], default="json", help="Output format: json or diff.")

    args = parser.parse_args()

    result = compare_suggestions(args.api_keys, args.prompt)

    if args.output == "json":
        print(json.dumps(result, indent=4))
    else:
        for key, diff in result["diffs"].items():
            print(f"\nComparison: {key}\n")
            print(diff)
