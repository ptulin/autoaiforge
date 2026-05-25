import ast
import json
from loguru import logger
import openai

def analyze_code(input_code_or_file):
    """
    Analyzes Python code for potential bugs using an AI-powered model.

    Args:
        input_code_or_file (str): Python code as a string or a file path to a Python script.

    Returns:
        dict: JSON report containing identified bugs and suggested fixes.
    """
    try:
        # Determine if input is a file or raw code
        if input_code_or_file.endswith('.py'):
            try:
                with open(input_code_or_file, 'r') as file:
                    code = file.read()
            except FileNotFoundError:
                logger.error("File not found.")
                return {
                    "error": "File not found.",
                    "details": "The specified file does not exist."
                }
        else:
            code = input_code_or_file

        # Parse the code to ensure it's valid Python
        try:
            ast.parse(code)
        except SyntaxError as e:
            return {
                "error": "Invalid Python code.",
                "details": str(e)
            }

        # Send code to OpenAI for analysis
        logger.info("Sending code to OpenAI for analysis...")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a Python debugging assistant."},
                    {"role": "user", "content": f"Analyze this Python code for potential bugs and suggest fixes: {code}"}
                ]
            )
        except openai.error.OpenAIError as e:
            logger.error("OpenAI API error: {}", e)
            return {
                "error": "OpenAI API error.",
                "details": str(e)
            }

        # Extract response
        suggestions = response['choices'][0]['message']['content']

        return {
            "code": code,
            "analysis": suggestions
        }

    except Exception as e:
        logger.error("Unexpected error: {}", e)
        return {
            "error": "Unexpected error.",
            "details": str(e)
        }

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Bug Sleuth: AI-powered Python code analysis tool.")
    parser.add_argument("input", type=str, help="Python script file or string input containing code.")
    args = parser.parse_args()

    result = analyze_code(args.input)
    print(json.dumps(result, indent=4))