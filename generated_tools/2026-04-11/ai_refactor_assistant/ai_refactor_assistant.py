import ast
import openai
import black
import os
import argparse

def refactor_code(input_code, output_file=None, openai_api_key=None):
    """
    Refactor Python code using AI suggestions and formatting.

    Args:
        input_code (str): Python code as a string or file path.
        output_file (str, optional): Path to save the refactored code. Defaults to None.
        openai_api_key (str, optional): OpenAI API key. Defaults to None.

    Returns:
        str: Refactored Python code.
    """
    if openai_api_key is None:
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OpenAI API key not provided. Set it as an argument or in the OPENAI_API_KEY environment variable.")

    # Load code from file if input_code is a file path
    if os.path.isfile(input_code):
        with open(input_code, "r") as file:
            input_code = file.read()

    # Validate input code using AST
    try:
        ast.parse(input_code)
    except SyntaxError as e:
        raise ValueError(f"Invalid Python code provided: {e}")

    # Call OpenAI API for suggestions
    openai.api_key = openai_api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a Python code refactoring assistant."},
                {"role": "user", "content": f"Refactor the following Python code for readability, performance, and best practices:\n\n{input_code}"}
            ]
        )
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

    # Extract the refactored code from the response
    try:
        refactored_code = response["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError("Unexpected response format from OpenAI API.")

    # Format the refactored code using Black
    try:
        refactored_code = black.format_str(refactored_code, mode=black.Mode())
    except black.InvalidInput as e:
        raise ValueError(f"Error formatting code with Black: {e}")

    # Save to file if output_file is specified
    if output_file:
        with open(output_file, "w") as file:
            file.write(refactored_code)

    return refactored_code

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Refactor Assistant: Refactor Python code using AI.")
    parser.add_argument("input_code", help="Path to the Python file to refactor or the Python code as a string.")
    parser.add_argument("--output_file", help="Path to save the refactored code.", default=None)
    parser.add_argument("--openai_api_key", help="OpenAI API key. If not provided, the OPENAI_API_KEY environment variable will be used.", default=None)
    args = parser.parse_args()

    try:
        refactored_code = refactor_code(args.input_code, args.output_file, args.openai_api_key)
        if not args.output_file:
            print(refactored_code)
    except Exception as e:
        print(f"Error: {e}")
