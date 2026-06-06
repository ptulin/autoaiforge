import argparse
import openai
import os

def get_code_completion(api_key, prompt, max_tokens=150):
    """
    Get code completion from OpenAI's API.

    Args:
        api_key (str): OpenAI API key.
        prompt (str): The input code snippet or file content.
        max_tokens (int): Maximum number of tokens for the completion.

    Returns:
        str: The completed code.
    """
    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=0.7
        )
        return response['choices'][0]['text'].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

def read_input_file(file_path):
    """
    Read the content of the input file.

    Args:
        file_path (str): Path to the input file.

    Returns:
        str: Content of the file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def main():
    parser = argparse.ArgumentParser(
        description="AI Code Completion CLI: Generate code completions using OpenAI's API."
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help="Path to the input file containing incomplete code or a code snippet."
    )
    parser.add_argument(
        '--api-key',
        type=str,
        required=True,
        help="Your OpenAI API key."
    )
    parser.add_argument(
        '--max-tokens',
        type=int,
        default=150,
        help="Maximum number of tokens to generate for the completion (default: 150)."
    )

    args = parser.parse_args()

    try:
        input_content = read_input_file(args.input)
        completion = get_code_completion(args.api_key, input_content, args.max_tokens)
        print("\n--- Code Completion ---\n")
        print(completion)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
