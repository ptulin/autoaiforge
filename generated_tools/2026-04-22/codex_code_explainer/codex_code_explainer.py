import openai
import textwrap
import argparse

def explain_code(code: str) -> str:
    """
    Uses OpenAI Codex to generate a human-readable explanation for the given Python code.

    Args:
        code (str): The Python code to explain.

    Returns:
        str: A formatted explanation of the code.
    """
    if not code.strip():
        return "Error: No code provided. Please provide valid Python code to explain."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Explain the following Python code in detail:\n\n{code}\n\nExplanation:",
            max_tokens=500,
            temperature=0.5
        )
        explanation = response.choices[0].text.strip()
        return textwrap.dedent(explanation)
    except openai.error.OpenAIError as e:
        return f"Error: Unable to generate explanation due to an API error: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Codex Code Explainer: Generate human-readable explanations for Python code using OpenAI Codex."
    )
    parser.add_argument(
        "code",
        type=str,
        help="The Python code to explain. Enclose the code in quotes."
    )
    args = parser.parse_args()

    explanation = explain_code(args.code)
    print(explanation)

if __name__ == "__main__":
    main()
