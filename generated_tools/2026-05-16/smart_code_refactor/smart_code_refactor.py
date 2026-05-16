import argparse
import os
import openai
from dotenv import load_dotenv
from diff_match_patch import diff_match_patch

def load_api_key():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return api_key

def refactor_code(file_path, goal):
    """
    Refactor the code in the given file based on the specified goal.

    Args:
        file_path (str): Path to the code file to refactor.
        goal (str): Refactoring goal (e.g., readability, performance, standards).

    Returns:
        str: Refactored code.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        original_code = file.read()

    if not original_code.strip():
        raise ValueError("The input file is empty.")

    openai.api_key = load_api_key()

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=(
                f"Refactor the following code to optimize for {goal}:\n\n"
                f"{original_code}\n"
            ),
            max_tokens=1500,
            temperature=0.7
        )
        refactored_code = response["choices"][0]["text"].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error while communicating with OpenAI API: {e}")

    return refactored_code

def display_diff(original_code, refactored_code):
    """
    Display the differences between the original and refactored code.

    Args:
        original_code (str): The original code.
        refactored_code (str): The refactored code.

    Returns:
        str: A unified diff string.
    """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(original_code, refactored_code)
    dmp.diff_cleanupSemantic(diffs)
    return dmp.diff_prettyHtml(diffs)

def main():
    parser = argparse.ArgumentParser(
        description="Smart Code Refactoring Tool: Optimize your code for readability, performance, or standards."
    )
    parser.add_argument(
        "--file",
        required=True,
        help="Path to the code file to refactor."
    )
    parser.add_argument(
        "--goal",
        required=True,
        choices=["readability", "performance", "standards"],
        help="Refactoring goal: readability, performance, or standards."
    )
    parser.add_argument(
        "--output",
        help="Path to save the refactored code. If not provided, the refactored code will be displayed."
    )
    args = parser.parse_args()

    try:
        with open(args.file, 'r') as file:
            original_code = file.read()

        refactored_code = refactor_code(args.file, args.goal)

        if args.output:
            with open(args.output, 'w') as output_file:
                output_file.write(refactored_code)
            print(f"Refactored code saved to {args.output}")
        else:
            print("Refactored Code:")
            print(refactored_code)

        print("\nChanges:")
        print(display_diff(original_code, refactored_code))

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
