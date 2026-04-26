import argparse
import os
import openai

# Set up OpenAI API key from environment variable
API_KEY = os.getenv('OPENAI_API_KEY', 'test_api_key')  # Default to a test key for testing purposes
if not API_KEY:
    raise EnvironmentError("OPENAI_API_KEY environment variable not set.")
openai.api_key = API_KEY

def generate_boilerplate(project_type):
    """Generate boilerplate code for a given project type using Claude AI."""
    prompt = f"Generate boilerplate code for a {project_type} Python project."
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error generating boilerplate: {e}")

def refactor_code(file_path):
    """Refactor and optimize code from a given file using Claude AI."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as file:
        code = file.read()

    prompt = f"Refactor and optimize the following Python code:\n{code}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error refactoring code: {e}")

def code_completion(context):
    """Provide in-line code completion suggestions using Claude AI."""
    prompt = f"Complete the following Python code:\n{context}"
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error providing code completion: {e}")

def main():
    """Main CLI entry point for Claude Code Assistant."""
    parser = argparse.ArgumentParser(description="Claude Code Assistant")
    parser.add_argument('--generate', type=str, help='Generate boilerplate code for a project type.')
    parser.add_argument('--refactor', type=str, help='Refactor and optimize code from a file.')
    parser.add_argument('--complete', type=str, help='Provide in-line code completion suggestions.')
    parser.add_argument('--output', type=str, help='Output file to save the result.')
    args = parser.parse_args()

    try:
        if args.generate:
            result = generate_boilerplate(args.generate)
        elif args.refactor:
            result = refactor_code(args.refactor)
        elif args.complete:
            result = code_completion(args.complete)
        else:
            print("No valid option provided. Use --help for usage details.")
            return

        if args.output:
            with open(args.output, 'w') as file:
                file.write(result)
            print(f"Result saved to {args.output}")
        else:
            print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
