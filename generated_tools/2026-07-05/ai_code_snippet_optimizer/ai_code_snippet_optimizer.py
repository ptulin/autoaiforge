import openai
from rich import print
import os

def optimize_code(code_snippet: str) -> dict:
    """
    Optimizes a Python code snippet using OpenAI's API.

    Args:
        code_snippet (str): The Python code snippet to optimize.

    Returns:
        dict: A dictionary containing the optimized code and an explanation of the changes.
    """
    if not code_snippet.strip():
        raise ValueError("The code snippet cannot be empty.")

    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise EnvironmentError("OPENAI_API_KEY environment variable is not set.")

    openai.api_key = openai_api_key

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer. Your task is to optimize Python code snippets for performance, readability, and maintainability. Provide detailed explanations for any changes you make."
                },
                {
                    "role": "user",
                    "content": f"Optimize the following Python code snippet:\n{code_snippet}"
                }
            ],
            temperature=0
        )

        ai_response = response['choices'][0]['message']['content']
        parts = ai_response.split("Explanation:", 1)
        if len(parts) != 2:
            raise ValueError("Unexpected response format from AI.")

        optimized_code = parts[0].strip()
        explanation = parts[1].strip()

        return {
            "optimized_code": optimized_code,
            "explanation": explanation
        }

    except openai.error.OpenAIError as e:
        raise RuntimeError(f"An error occurred while communicating with the OpenAI API: {e}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI Code Snippet Optimizer")
    parser.add_argument("code_snippet", type=str, help="The Python code snippet to optimize.")
    args = parser.parse_args()

    try:
        result = optimize_code(args.code_snippet)
        print("[bold green]Optimized Code:[/bold green]")
        print(result["optimized_code"])
        print("\n[bold blue]Explanation:[/bold blue]")
        print(result["explanation"])
    except Exception as e:
        print(f"[bold red]Error:[/bold red] {e}")