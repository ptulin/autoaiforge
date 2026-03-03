import argparse
import openai
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

def analyze_error(script_content, error_message):
    """
    Analyze the provided Python script and error message using OpenAI's Claude Opus.

    Args:
        script_content (str): The content of the Python script.
        error_message (str): The error message or stack trace.

    Returns:
        str: AI-suggested fixes and explanations.
    """
    try:
        prompt = (
            "You are an AI assistant specialized in debugging Python code. "
            "Analyze the following script and error message, identify the root cause, "
            "and suggest actionable fixes.\n\n"
            f"Script:\n{script_content}\n\nError:\n{error_message}\n"
        )

        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )

        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error during AI analysis: {str(e)}"

def read_file(file_path):
    """
    Read the content of a file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: Content of the file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Error: File not found."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def main():
    parser = argparse.ArgumentParser(description="Debugging AI Assistant")
    parser.add_argument('--file', type=str, required=True, help="Path to the Python script file.")
    parser.add_argument('--error', type=str, required=True, help="Error message or stack trace.")
    args = parser.parse_args()

    script_content = read_file(args.file)
    if script_content.startswith("Error:"):
        print(script_content)
        return

    suggestions = analyze_error(script_content, args.error)

    print("\nAI Suggestions:")
    print(highlight(suggestions, PythonLexer(), TerminalFormatter()))

if __name__ == "__main__":
    main()