import re
import argparse
from colorama import Fore, Style

def detect_prompt_injection(prompt):
    """
    Analyze the given prompt for signs of malicious injections.

    Args:
        prompt (str): The input prompt to analyze.

    Returns:
        dict: A dictionary containing the risk score and suggestions.
    """
    if not prompt.strip():
        return {"risk_score": 0, "suggestions": ["Prompt is empty."]}

    patterns = [
        r"ignore previous instructions",  # Common override phrase
        r"disregard all prior rules",     # Another override phrase
        r"pretend to be",                 # Impersonation attempt
        r"you are now",                   # Attempt to redefine behavior
        r"forget everything I said",      # Instruction to forget context
    ]

    risk_score = 0
    matched_patterns = []

    for pattern in patterns:
        if re.search(pattern, prompt, re.IGNORECASE):
            matched_patterns.append(pattern)
            risk_score += 20

    risk_score = min(risk_score, 100)  # Cap the risk score at 100

    suggestions = []
    if matched_patterns:
        suggestions.append("Avoid using phrases that override instructions.")
        suggestions.append("Rephrase the prompt to be more specific and constrained.")
    else:
        suggestions.append("No issues detected.")

    return {"risk_score": risk_score, "suggestions": suggestions}

def main():
    parser = argparse.ArgumentParser(
        description="Prompt Injection Detector: Analyze LLM prompts for malicious injections."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        help="The LLM prompt to analyze.",
    )

    args = parser.parse_args()

    if args.prompt:
        result = detect_prompt_injection(args.prompt)
        print(Fore.YELLOW + f"Risk Score: {result['risk_score']}" + Style.RESET_ALL)
        print(Fore.GREEN + "Suggestions:" + Style.RESET_ALL)
        for suggestion in result['suggestions']:
            print(f"- {suggestion}")
    else:
        print(Fore.RED + "Error: No prompt provided. Use --prompt to specify a prompt." + Style.RESET_ALL)

if __name__ == "__main__":
    main()