import json
import re
from typing import Union, Dict, Any

def sanitize(payload: Union[str, Dict[str, Any]], rules: Dict[str, str] = None) -> Union[str, Dict[str, Any]]:
    """
    Sanitizes potentially unsafe user inputs based on customizable rules.

    Args:
        payload (Union[str, Dict[str, Any]]): Raw user input or JSON payload.
        rules (Dict[str, str], optional): Custom sanitization rules as regex patterns and replacements.

    Returns:
        Union[str, Dict[str, Any]]: Sanitized input ready for safe API consumption.
    """
    if rules is None:
        # Default rules for sanitization
        rules = {
            r"(?i)drop\s+database": "[REDACTED]",
            r"(?i)delete\s+from": "[REDACTED]",
            r"(?i)select\s+\*": "[REDACTED]",
        }

    def apply_rules(text: str) -> str:
        for pattern, replacement in rules.items():
            text = re.sub(pattern, replacement, text)
        return text

    if isinstance(payload, str):
        return apply_rules(payload)
    elif isinstance(payload, dict):
        sanitized_payload = {}
        for key, value in payload.items():
            if isinstance(value, str):
                sanitized_payload[key] = apply_rules(value)
            elif isinstance(value, dict):
                sanitized_payload[key] = sanitize(value, rules)
            else:
                sanitized_payload[key] = value
        return sanitized_payload
    else:
        raise ValueError("Payload must be a string or a dictionary.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Payload Sanitizer")
    parser.add_argument("input", type=str, help="Raw user input or JSON payload as a string")
    args = parser.parse_args()

    try:
        input_data = json.loads(args.input)
    except json.JSONDecodeError:
        input_data = args.input

    sanitized = sanitize(input_data)
    print(json.dumps(sanitized, indent=2))