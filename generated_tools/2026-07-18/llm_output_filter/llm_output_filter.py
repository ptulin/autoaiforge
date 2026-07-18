import re
import json
from transformers import pipeline

def filter_output(text, rules=None, rules_file=None):
    """
    Filters the output text based on provided rules or a rules file.

    Args:
        text (str): The text to be filtered.
        rules (dict, optional): A dictionary of filtering rules.
        rules_file (str, optional): Path to a JSON file containing filtering rules.

    Returns:
        str: The filtered text with sensitive content redacted.
    """
    if not text or not isinstance(text, str):
        raise ValueError("Input text must be a non-empty string.")

    if rules_file:
        try:
            with open(rules_file, 'r') as f:
                rules = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError("Invalid rules file.") from e

    if not rules or not isinstance(rules, dict):
        raise ValueError("Rules must be a dictionary or a valid JSON file.")

    for pattern, replacement in rules.items():
        try:
            text = re.sub(pattern, replacement, text)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {pattern}") from e

    return text

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="LLM Output Filter Tool")
    parser.add_argument("text", type=str, help="The text to filter.")
    parser.add_argument("--rules", type=str, help="JSON string of filtering rules.")
    parser.add_argument("--rules_file", type=str, help="Path to a JSON file containing filtering rules.")

    args = parser.parse_args()

    rules = None
    if args.rules:
        try:
            rules = json.loads(args.rules)
        except json.JSONDecodeError:
            print("Invalid JSON string for rules.")
            exit(1)

    try:
        filtered_text = filter_output(args.text, rules=rules, rules_file=args.rules_file)
        print(filtered_text)
    except ValueError as e:
        print(f"Error: {e}")
        exit(1)