import argparse
import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import os

def analyze_code(api_key, code):
    """
    Analyze the provided code using OpenAI's API.

    Args:
        api_key (str): OpenAI API key.
        code (str): Code snippet to analyze.

    Returns:
        str: AI-generated feedback on the code.
    """
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following Python code for bugs, optimizations, and adherence to best practices:\n\n{code}\n\nProvide actionable feedback with explanations:",
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def read_code_from_file(file_path):
    """
    Read code from a given file.

    Args:
        file_path (str): Path to the code file.

    Returns:
        str: Content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(
        description="AI Code Review: Analyze Python code for bugs, optimizations, and best practices."
    )
    parser.add_argument('--file', type=str, help="Path to the Python file to analyze.")
    parser.add_argument('--code', type=str, help="Python code snippet to analyze.")
    parser.add_argument('--api-key', type=str, required=True, help="Your OpenAI API key.")

    args = parser.parse_args()

    if not args.file and not args.code:
        print("Error: You must provide either a file path (--file) or a code snippet (--code).")
        return

    if args.file:
        try:
            code = read_code_from_file(args.file)
        except FileNotFoundError as e:
            print(e)
            return
    else:
        code = args.code

    print("Analyzing code...")
    feedback = analyze_code(args.api_key, code)

    print("\nAnalysis Feedback:")
    print("=" * 40)
    print(highlight(feedback, PythonLexer(), TerminalFormatter()))

if __name__ == "__main__":
    main()