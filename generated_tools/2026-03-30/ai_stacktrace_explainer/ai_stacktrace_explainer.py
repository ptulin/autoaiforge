import argparse
import sys
import os
from openai import ChatCompletion
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="AI Stacktrace Explainer: Analyze stack traces and provide explanations with resolution suggestions."
    )
    parser.add_argument(
        '--tracefile',
        type=str,
        help='Path to a file containing the stack trace.',
    )
    parser.add_argument(
        '--output',
        type=str,
        help='Optional path to save the explanation output.',
    )
    return parser.parse_args()

def read_stack_trace(tracefile):
    if not os.path.exists(tracefile):
        raise FileNotFoundError(f"The file '{tracefile}' does not exist.")
    with open(tracefile, 'r') as file:
        return file.read()

def explain_stack_trace(stack_trace):
    """Use OpenAI's API to explain the stack trace."""
    try:
        import openai
        openai.api_key = os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")

        response = ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python developer who explains stack traces."},
                {"role": "user", "content": f"Please explain the following Python stack trace and provide suggestions to fix it:\n{stack_trace}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error while communicating with OpenAI API: {e}"

def main():
    args = parse_arguments()

    if args.tracefile:
        try:
            stack_trace = read_stack_trace(args.tracefile)
        except Exception as e:
            print(f"Error reading stack trace file: {e}")
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Error: No input provided. Use --tracefile or pipe a stack trace to the script.")
            sys.exit(1)
        stack_trace = sys.stdin.read()

    explanation = explain_stack_trace(stack_trace)

    if args.output:
        try:
            with open(args.output, 'w') as output_file:
                output_file.write(explanation)
            print(f"Explanation saved to {args.output}")
        except Exception as e:
            print(f"Error saving explanation to file: {e}")
            sys.exit(1)
    else:
        print("\nExplanation:")
        print(highlight(explanation, PythonLexer(), TerminalFormatter()))

if __name__ == "__main__":
    main()
