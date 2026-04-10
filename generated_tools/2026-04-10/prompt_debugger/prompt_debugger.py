import openai
import typer
from typing import List

def analyze_prompt(prompt: str, model: str) -> str:
    """
    Analyzes the given prompt for weaknesses by generating edge cases and evaluating responses.

    Args:
        prompt (str): The input prompt to analyze.
        model (str): The target AI model to use.

    Returns:
        str: A detailed diagnostic report with improvement suggestions.
    """
    try:
        # Generate edge cases for the prompt
        edge_cases = [
            prompt + " (in a humorous tone)",
            prompt + " (in one sentence)",
            prompt + " (with a twist ending)",
            prompt + " (as a poem)",
            prompt + " (in the style of Shakespeare)",
        ]

        responses = []

        for case in edge_cases:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": case}]
            )
            responses.append({"case": case, "response": response["choices"][0]["message"]["content"]})

        # Analyze responses for consistency and ambiguity
        analysis = []
        for item in responses:
            response_text = item['response']
            if len(response_text.strip()) == 0:
                analysis.append(f"Edge case '{item['case']}' produced an empty response.")
            elif "error" in response_text.lower():
                analysis.append(f"Edge case '{item['case']}' resulted in an error-like response.")
            else:
                analysis.append(f"Edge case '{item['case']}' produced a valid response.")

        # Generate diagnostic report
        report = "Prompt Diagnostic Report:\n"
        report += "\n".join(analysis)
        report += "\n\nSuggestions for Improvement:\n"
        report += "- Ensure the prompt is clear and unambiguous.\n"
        report += "- Test prompts with different tones and formats to identify weaknesses.\n"
        report += "- Avoid overly complex or vague instructions.\n"

        return report

    except openai.error.OpenAIError as e:
        return f"An error occurred while interacting with the OpenAI API: {e}"

app = typer.Typer()

@app.command()
def main(prompt: str = typer.Option(..., help="The prompt to analyze."),
         model: str = typer.Option("gpt-3.5-turbo", help="The target AI model to use.")):
    """
    CLI entry point for the Prompt Debugger tool.

    Args:
        prompt (str): The input prompt to analyze.
        model (str): The target AI model to use.
    """
    report = analyze_prompt(prompt, model)
    typer.echo(report)

if __name__ == "__main__":
    app()
