import argparse
import os
import openai
from dotenv import load_dotenv

def lint_code(file_path):
    """
    Lint the code in the given file using OpenAI Codex.

    Args:
        file_path (str): Path to the code file.

    Returns:
        str: Linting suggestions and explanations.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        code_content = file.read()

    if not code_content.strip():
        return "The file is empty. No code to lint."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Lint the following code and provide suggestions with explanations:\n\n{code_content}",
            max_tokens=1000,
            temperature=0.7
        )
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['text'].strip()
        else:
            return "No suggestions returned by the AI."
    except openai.error.OpenAIError as e:
        return f"Error while communicating with OpenAI API: {str(e)}"


def main():
    """
    Main function to parse arguments and execute the linting tool.
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    parser = argparse.ArgumentParser(
        description="AI-Powered Code Linter: Provides intelligent code linting suggestions using OpenAI Codex."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the code file to lint."
    )

    args = parser.parse_args()
    file_path = args.file

    try:
        suggestions = lint_code(file_path)
        print("Linting Suggestions:\n")
        print(suggestions)
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
