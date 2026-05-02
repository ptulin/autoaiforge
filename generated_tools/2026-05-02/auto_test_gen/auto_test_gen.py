import argparse
import os
import openai

def generate_tests(source_code_or_path, output_file=None, openai_api_key=None):
    """
    Generate pytest-compatible test cases for the given Python source code.

    Args:
        source_code_or_path (str): Python source code as a string or a file path.
        output_file (str, optional): Path to save the generated test cases. If None, returns the test code as a string.
        openai_api_key (str, optional): OpenAI API key. If not provided, it will look for OPENAI_API_KEY in environment variables.

    Returns:
        str: Generated pytest-compatible test code if output_file is None.
    """
    # Retrieve OpenAI API key
    api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API key must be provided either as an argument or in the OPENAI_API_KEY environment variable.")

    openai.api_key = api_key

    # Read source code from file if a file path is provided
    if os.path.isfile(source_code_or_path):
        try:
            with open(source_code_or_path, 'r') as f:
                source_code = f.read()
        except FileNotFoundError:
            raise ValueError(f"File not found: {source_code_or_path}")
    else:
        source_code = source_code_or_path

    # Use OpenAI API to generate test cases
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate pytest-compatible unit tests for the following Python code:\n\n{source_code}\n\n",
            max_tokens=1500,
            temperature=0.3
        )
        test_code = response["choices"][0]["text"].strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Failed to generate tests using OpenAI API: {e}")

    # Save to file or return as string
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(test_code)
        except Exception as e:
            raise RuntimeError(f"Failed to write test cases to file: {e}")
    else:
        return test_code


def main():
    parser = argparse.ArgumentParser(description="Auto Test Generator: Generate pytest-compatible test cases using OpenAI API.")
    parser.add_argument("source", help="Path to the Python source code file or the source code as a string.")
    parser.add_argument("--output", help="Path to save the generated test cases.", default=None)
    parser.add_argument("--api-key", help="OpenAI API key. If not provided, will use the OPENAI_API_KEY environment variable.", default=None)

    args = parser.parse_args()

    try:
        generate_tests(args.source, output_file=args.output, openai_api_key=args.api_key)
        print("Test cases generated successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
