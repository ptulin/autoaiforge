import argparse
import openai
import black
import os

def optimize_code(file_path, api_key):
    """
    Optimizes the given Python script for performance and readability.

    Args:
        file_path (str): Path to the Python script to be optimized.
        api_key (str): OpenAI API key for generating suggestions.

    Returns:
        tuple: Optimized code (str) and a change log (str).
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        original_code = file.read()

    if not original_code.strip():
        raise ValueError("The provided file is empty.")

    # Format the code using Black
    try:
        formatted_code = black.format_str(original_code, mode=black.FileMode())
    except black.InvalidInput as e:
        raise ValueError(f"The provided code is invalid: {e}")

    # Generate AI suggestions using OpenAI
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert Python developer. Provide performance and readability improvements for the following code. Include explanations for each change.",
                },
                {"role": "user", "content": formatted_code},
            ],
        )
    except Exception as e:
        raise ConnectionError(f"Failed to connect to OpenAI API: {e}")

    suggestions = response['choices'][0]['message']['content']

    return formatted_code, suggestions

def main():
    parser = argparse.ArgumentParser(
        description="Code Optimizer Agent: Analyze and optimize Python scripts for performance and readability."
    )
    parser.add_argument(
        "--file", required=True, help="Path to the Python script file to optimize."
    )
    parser.add_argument(
        "--api-key", required=True, help="Your OpenAI API key for generating suggestions."
    )

    args = parser.parse_args()

    try:
        optimized_code, change_log = optimize_code(args.file, args.api_key)

        optimized_file_path = f"optimized_{os.path.basename(args.file)}"
        with open(optimized_file_path, 'w') as file:
            file.write(optimized_code)

        change_log_path = f"change_log_{os.path.basename(args.file)}.txt"
        with open(change_log_path, 'w') as file:
            file.write(change_log)

        print(f"Optimized code saved to: {optimized_file_path}")
        print(f"Change log saved to: {change_log_path}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
