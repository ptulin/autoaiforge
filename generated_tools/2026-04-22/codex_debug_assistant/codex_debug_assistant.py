import argparse
import openai
from rich.console import Console
from rich.text import Text

def get_codex_suggestions(prompt: str, api_key: str) -> str:
    """
    Query the OpenAI Codex API with a given prompt and return the response.

    Args:
        prompt (str): The input prompt to send to Codex.
        api_key (str): OpenAI API key.

    Returns:
        str: The response from Codex.
    """
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=300,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error communicating with OpenAI API: {str(e)}"

def process_input(input_text: str, api_key: str) -> str:
    """
    Process the input text and return Codex suggestions.

    Args:
        input_text (str): The error message, stack trace, or code snippet.
        api_key (str): OpenAI API key.

    Returns:
        str: Suggestions from Codex.
    """
    if not input_text.strip():
        return "Error: Input text is empty. Please provide a valid error message, stack trace, or code snippet."

    prompt = (
        "You are an AI assistant specialized in debugging Python code. "
        "Given the following input, provide detailed explanations, possible fixes, "
        "and relevant test cases to diagnose the issue effectively.\n\n"
        f"Input:\n{input_text}\n\n"
        "Output:"
    )
    return get_codex_suggestions(prompt, api_key)

def main():
    parser = argparse.ArgumentParser(
        description="Codex Debug Assistant: Get debugging help from OpenAI Codex."
    )
    parser.add_argument(
        "--input",
        type=str,
        required=True,
        help="Error message, stack trace, or code snippet to debug."
    )
    parser.add_argument(
        "--api_key",
        type=str,
        required=True,
        help="Your OpenAI API key."
    )

    args = parser.parse_args()

    console = Console()
    console.print(Text("Codex Debug Assistant", style="bold green"))

    suggestions = process_input(args.input, args.api_key)

    console.print(Text("\nSuggestions:", style="bold blue"))
    console.print(suggestions)

if __name__ == "__main__":
    main()
