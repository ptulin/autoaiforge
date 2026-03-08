import os
import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter
import argparse

def analyze_codebase(directory_path, openai_api_key):
    """
    Analyze a codebase for bugs, optimizations, and documentation improvements using GPT-5.4.

    Args:
        directory_path (str): Path to the root directory of the codebase.
        openai_api_key (str): OpenAI API key for accessing GPT-5.4.

    Returns:
        None: Prints annotated code files or suggested changes to stdout.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"The path '{directory_path}' is not a valid directory.")

    openai.api_key = openai_api_key

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r') as f:
                        code_content = f.read()

                    response = openai.Completion.create(
                        engine="gpt-5.4",
                        prompt=f"Analyze the following Python code for bugs, optimizations, and documentation improvements:\n\n{code_content}",
                        max_tokens=1000,
                        temperature=0.7
                    )

                    suggestions = response.choices[0].text.strip()

                    print(f"\nSuggestions for {file_path}:\n")
                    print(highlight(suggestions, PythonLexer(), TerminalFormatter()))

                except Exception as e:
                    print(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze a Python codebase using GPT-5.4.")
    parser.add_argument("directory", type=str, help="Path to the root directory of the codebase.")
    parser.add_argument("api_key", type=str, help="OpenAI API key.")

    args = parser.parse_args()

    try:
        analyze_codebase(args.directory, args.api_key)
    except Exception as e:
        print(f"Error: {e}")