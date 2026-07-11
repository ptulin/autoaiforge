import argparse
import openai
import tiktoken
from unittest.mock import patch, MagicMock

def count_tokens(text, encoding_name="cl100k_base"):
    """Count the number of tokens in a given text using the specified encoding."""
    try:
        encoding = tiktoken.get_encoding(encoding_name)
        return len(encoding.encode(text))
    except Exception as e:
        raise ValueError(f"Error counting tokens: {e}")

def optimize_text(api_key, input_text):
    """Optimize the input text using OpenAI's API to minimize token usage."""
    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rewrite the following text to minimize token usage while retaining its original meaning."},
                {"role": "user", "content": input_text}
            ]
        )
        optimized_text = response.choices[0].message.content.strip()
        return optimized_text
    except Exception as e:
        raise RuntimeError(f"Error optimizing text: {e}")

def process_input(input_path):
    """Read input text from a file or return the inline text."""
    try:
        with open(input_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Input file '{input_path}' not found.")

def main():
    parser = argparse.ArgumentParser(
        description="Token Optimizer Rewriter: Minimize token usage while retaining text meaning."
    )
    parser.add_argument("--input", required=True, help="Path to input text file or inline text.")
    parser.add_argument("--api_key", required=True, help="API key for OpenAI integration.")
    args = parser.parse_args()

    input_text = args.input
    api_key = args.api_key

    try:
        # Check if input is a file path or inline text
        if input_text.endswith(".txt"):
            input_text = process_input(input_text)

        original_token_count = count_tokens(input_text)
        optimized_text = optimize_text(api_key, input_text)
        optimized_token_count = count_tokens(optimized_text)

        print("Original Text:")
        print(input_text)
        print(f"Token Count: {original_token_count}\n")

        print("Optimized Text:")
        print(optimized_text)
        print(f"Token Count: {optimized_token_count}\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()