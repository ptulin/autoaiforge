import argparse
import json
import os
from openai.error import OpenAIError
from openai import ChatCompletion
import openai

def analyze_code_with_ai(api_key, code_snippet, language="Python"):
    """
    Analyze the provided code snippet using OpenAI's API.

    Args:
        api_key (str): OpenAI API key.
        code_snippet (str): The code snippet to analyze.
        language (str): Programming language of the code.

    Returns:
        str: AI-generated review and suggestions.
    """
    try:
        openai.api_key = api_key
        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": f"You are an expert code reviewer for {language} code."},
                {"role": "user", "content": f"Please review the following {language} code and provide suggestions for improvement, optimization, and error fixes:\n\n{code_snippet}"}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except OpenAIError as e:
        return f"Error communicating with OpenAI API: {str(e)}"

def load_code_from_file(file_path):
    """
    Load code from a file.

    Args:
        file_path (str): Path to the file containing the code.

    Returns:
        str: Content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Assistant")
    parser.add_argument("--file", type=str, help="Path to the code file to review.")
    parser.add_argument("--code", type=str, help="Code snippet to review.")
    parser.add_argument("--save", type=str, help="Path to save the review output as a JSON file.")
    parser.add_argument("--api-key", type=str, required=True, help="OpenAI API key.")
    parser.add_argument("--language", type=str, default="Python", help="Programming language of the code (default: Python).")

    args = parser.parse_args()

    if not args.file and not args.code:
        print("Error: Either --file or --code must be provided.")
        return

    if args.file:
        try:
            code_snippet = load_code_from_file(args.file)
        except FileNotFoundError as e:
            print(e)
            return
    else:
        code_snippet = args.code

    print("Analyzing code... This may take a moment.")
    review = analyze_code_with_ai(args.api_key, code_snippet, args.language)

    if args.save:
        try:
            with open(args.save, "w", encoding="utf-8") as file:
                json.dump({"review": review}, file, indent=4)
            print(f"Review saved to {args.save}")
        except Exception as e:
            print(f"Error saving the review: {str(e)}")
    else:
        print("\nAI Code Review:\n")
        print(review)

if __name__ == "__main__":
    main()
