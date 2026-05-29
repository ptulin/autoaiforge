import os
import argparse
import openai
from dotenv import load_dotenv

def load_api_key():
    """Load the OpenAI API key from environment variables."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    return api_key

def refactor_code(file_path):
    """Refactor code using OpenAI API."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        code_content = file.read()

    if not code_content.strip():
        raise ValueError("The file is empty.")

    api_key = load_api_key()
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Refactor the following code for better readability and optimization:\n{code_content}",
            max_tokens=1500
        )
        if not response or not response.get("choices") or not response["choices"]:
            raise RuntimeError("Invalid response from OpenAI API.")
        return response["choices"][0]["text"].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

def main():
    parser = argparse.ArgumentParser(description="AI Code Refactorer - Refactor your code using OpenAI.")
    parser.add_argument('--file', type=str, required=True, help="Path to the file to be refactored.")
    parser.add_argument('--save', type=str, help="Path to save the refactored code.")

    args = parser.parse_args()

    try:
        refactored_code = refactor_code(args.file)
        if args.save:
            with open(args.save, 'w') as save_file:
                save_file.write(refactored_code)
            print(f"Refactored code saved to {args.save}")
        else:
            print("Refactored Code:")
            print(refactored_code)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
