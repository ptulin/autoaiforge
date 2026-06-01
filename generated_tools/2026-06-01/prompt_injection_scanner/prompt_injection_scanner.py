import argparse
import json
import regex as re
from typing import List, Dict

def detect_prompt_injection(text: str, patterns: List[str]) -> List[Dict[str, str]]:
    """
    Detect potential prompt injection patterns in the given text.

    Args:
        text (str): The input text to scan.
        patterns (List[str]): A list of regex patterns to detect prompt injection.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'line' and 'reason' keys for flagged inputs.
    """
    flagged = []
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            flagged.append({"line": match.group(0), "reason": f"Matched pattern: {pattern}"})
    return flagged

def scan_file(file_path: str, patterns: List[str]) -> List[Dict[str, str]]:
    """
    Scan a file for potential prompt injection patterns.

    Args:
        file_path (str): Path to the file to scan.
        patterns (List[str]): A list of regex patterns to detect prompt injection.

    Returns:
        List[Dict[str, str]]: A list of dictionaries with 'line' and 'reason' keys for flagged inputs.
    """
    flagged = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                flagged.extend(detect_prompt_injection(line.strip(), patterns))
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the file: {e}")
    return flagged

def main():
    parser = argparse.ArgumentParser(description="Prompt Injection Scanner")
    parser.add_argument('--input', required=True, help="Path to the input file or a single text input")
    parser.add_argument('--output', help="Path to the output JSON file")
    parser.add_argument('--patterns', nargs='*', default=[
        r"(?i)ignore\s+all\s+previous\s+instructions",
        r"(?i)delete\s+all\s+data",
        r"(?i)execute\s+command",
        r"(?i)shutdown\s+system"
    ], help="Custom regex patterns for detecting prompt injection")

    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    patterns = args.patterns

    try:
        if '\n' in input_path or len(input_path.splitlines()) > 1:
            # Treat as direct text input
            flagged_results = detect_prompt_injection(input_path, patterns)
        else:
            # Treat as a file path
            flagged_results = scan_file(input_path, patterns)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as output_file:
                json.dump(flagged_results, output_file, indent=4)
            print(f"Results written to {output_path}")
        else:
            print(json.dumps(flagged_results, indent=4))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()