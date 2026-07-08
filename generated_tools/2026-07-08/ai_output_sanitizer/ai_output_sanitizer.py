import argparse
import re
import json
import sys
from colorama import Fore, Style

def load_rules(rules_path):
    """Load detection rules from a JSON file."""
    try:
        with open(rules_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Rules file not found: {rules_path}{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Invalid JSON in rules file: {rules_path}{Style.RESET_ALL}")
        sys.exit(1)

def sanitize_text(text, rules, mask):
    """Scan and sanitize text based on rules."""
    sanitized_text = text
    flagged_items = []

    for rule in rules:
        pattern = rule.get("pattern")
        description = rule.get("description", "Sensitive data")

        if not pattern:
            continue

        matches = re.findall(pattern, text)
        for match in matches:
            flagged_items.append((match, description))
            if mask:
                sanitized_text = re.sub(re.escape(match), "[REDACTED]", sanitized_text)

    return sanitized_text, flagged_items

def main():
    parser = argparse.ArgumentParser(description="AI Output Sanitizer")
    parser.add_argument("--input", help="Path to the input text file", required=True)
    parser.add_argument("--rules", help="Path to the JSON rules file", required=True)
    parser.add_argument("--mask", help="Mask sensitive data instead of just flagging", action="store_true")

    args = parser.parse_args()

    try:
        with open(args.input, 'r') as f:
            input_text = f.read()
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Input file not found: {args.input}{Style.RESET_ALL}")
        sys.exit(1)

    rules = load_rules(args.rules)

    sanitized_text, flagged_items = sanitize_text(input_text, rules, args.mask)

    if flagged_items:
        print(f"{Fore.YELLOW}Flagged sensitive data:{Style.RESET_ALL}")
        for item, description in flagged_items:
            print(f"- {description}: {item}")

    print(f"{Fore.GREEN}Sanitized Output:{Style.RESET_ALL}\n")
    print(sanitized_text)

if __name__ == "__main__":
    main()
