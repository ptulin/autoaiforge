import argparse
import json
import requests
from typing import List, Dict

def fetch_ai_feedback(api_url: str, api_key: str, code: str) -> Dict:
    """
    Fetch feedback from an AI reviewer.

    Args:
        api_url (str): The API endpoint for the AI reviewer.
        api_key (str): The API key for authentication.
        code (str): The code to be reviewed.

    Returns:
        Dict: The feedback from the AI reviewer.
    """
    try:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {api_key}"},
            json={"code": code}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def aggregate_feedback(feedback_list: List[Dict]) -> Dict:
    """
    Aggregate feedback from multiple AI reviewers.

    Args:
        feedback_list (List[Dict]): List of feedback dictionaries.

    Returns:
        Dict: Aggregated feedback.
    """
    aggregated = {}
    for feedback in feedback_list:
        for key, value in feedback.items():
            if key not in aggregated:
                aggregated[key] = []
            aggregated[key].append(value)
    return aggregated

def filter_feedback(aggregated_feedback: Dict, filters: List[str]) -> Dict:
    """
    Filter aggregated feedback based on user-defined filters.

    Args:
        aggregated_feedback (Dict): Aggregated feedback from AI reviewers.
        filters (List[str]): List of filters to apply.

    Returns:
        Dict: Filtered feedback.
    """
    if not filters:
        return aggregated_feedback

    filtered = {}
    for key, values in aggregated_feedback.items():
        if key in filters:
            filtered[key] = values
    return filtered

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Pipeline")
    parser.add_argument("--file", required=True, help="Path to the code file to be reviewed.")
    parser.add_argument("--config", required=True, help="Path to the reviewer configuration JSON file.")
    parser.add_argument("--filters", nargs="*", help="List of feedback categories to include.")

    args = parser.parse_args()

    try:
        # Load code file
        with open(args.file, "r") as code_file:
            code = code_file.read()

        # Load reviewer configuration
        with open(args.config, "r") as config_file:
            config = json.load(config_file)

        feedback_list = []

        for reviewer in config.get("reviewers", []):
            api_url = reviewer.get("api_url")
            api_key = reviewer.get("api_key")

            if not api_url or not api_key:
                print(f"Skipping reviewer with missing API details: {reviewer}")
                continue

            feedback = fetch_ai_feedback(api_url, api_key, code)
            feedback_list.append(feedback)

        aggregated_feedback = aggregate_feedback(feedback_list)
        filtered_feedback = filter_feedback(aggregated_feedback, args.filters)

        print(json.dumps(filtered_feedback, indent=4))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()