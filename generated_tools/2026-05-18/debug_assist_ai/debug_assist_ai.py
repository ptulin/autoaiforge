import argparse
import sys
import openai

def analyze_error_message(error_message):
    """
    Analyze the error message or stack trace using OpenAI's API to generate suggestions.

    Args:
        error_message (str): The error message or stack trace to analyze.

    Returns:
        str: AI-generated suggestions for debugging and fixing the error.
    """
    try:
        # Call OpenAI's API to get suggestions
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following Python error message or stack trace and provide suggestions for fixing it:\n{error_message}\n",
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error communicating with OpenAI API: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def main():
    parser = argparse.ArgumentParser(
        description="Debug Assist AI: Analyze error messages or stack traces and generate AI-powered suggestions for fixing them."
    )
    parser.add_argument(
        '--error_message', '-e',
        type=str,
        help='The error message or stack trace to analyze.'
    )

    args = parser.parse_args()

    if args.error_message:
        error_message = args.error_message
    elif not sys.stdin.isatty():
        error_message = sys.stdin.read().strip()
    else:
        print("Error: No error message provided. Use --error_message or pipe input.", file=sys.stderr)
        sys.exit(1)

    suggestions = analyze_error_message(error_message)
    print("\nAI Suggestions:\n")
    print(suggestions)

if __name__ == "__main__":
    main()