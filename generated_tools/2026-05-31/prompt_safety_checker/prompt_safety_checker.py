import typer
from typing import List

# Initialize the CLI app
app = typer.Typer()

# Default safety rules for prompt analysis
DEFAULT_SAFETY_RULES = [
    "contains hate speech",
    "contains explicit content",
    "incites violence",
    "contains discriminatory language"
]

def analyze_prompt(prompt: str, safety_rules: List[str]) -> dict:
    """
    Analyze the given prompt against safety rules.

    Args:
        prompt (str): The text prompt to analyze.
        safety_rules (list[str]): List of safety rules to check against.

    Returns:
        dict: A dictionary containing flagged issues and suggestions.
    """
    flagged_issues = []

    try:
        # Mocked sentiment analysis result for testing purposes
        sentiment_label = "POSITIVE"  # Default to positive sentiment
        if "hate" in prompt.lower() or "angry" in prompt.lower():
            sentiment_label = "NEGATIVE"

        # Check against safety rules
        for rule in safety_rules:
            if rule in prompt.lower():
                flagged_issues.append(rule)

        # Add sentiment analysis results
        if sentiment_label == "NEGATIVE":
            flagged_issues.append("Negative sentiment detected")

    except Exception as e:
        return {"error": str(e)}

    return {
        "flagged_issues": flagged_issues,
        "suggestions": "Consider rephrasing or removing flagged content."
    }

@app.command()
def check_prompt(prompt: str, interactive: bool = False):
    """
    Check the safety of a given prompt.

    Args:
        prompt (str): The text prompt to analyze.
        interactive (bool): Enable interactive mode for real-time feedback.
    """
    safety_rules = DEFAULT_SAFETY_RULES

    if interactive:
        typer.echo("Interactive mode enabled. Type 'exit' to quit.")
        while True:
            user_prompt = typer.prompt("Enter a prompt")
            if user_prompt.lower() == "exit":
                typer.echo("Exiting interactive mode.")
                break
            result = analyze_prompt(user_prompt, safety_rules)
            typer.echo(result)
    else:
        result = analyze_prompt(prompt, safety_rules)
        typer.echo(result)

if __name__ == "__main__":
    app()
