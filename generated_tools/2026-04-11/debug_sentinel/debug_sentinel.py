import traceback
import json
import argparse
from openai import ChatCompletion

class DebugSentinel:
    def __init__(self, api_key):
        self.api_key = api_key

    def suggest_fix(self, stack_trace, output_format="text"):
        """
        Analyze the provided stack trace and return suggested fixes.

        Args:
            stack_trace (str): The Python exception stack trace.
            output_format (str): Output format, either 'text' or 'json'.

        Returns:
            str: Suggested fixes in the specified format.
        """
        if not stack_trace.strip():
            raise ValueError("Stack trace cannot be empty.")

        try:
            response = ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI assistant that helps debug Python errors."},
                    {"role": "user", "content": f"Analyze this stack trace and suggest fixes:\n{stack_trace}"}
                ]
            )

            suggestions = response["choices"][0]["message"]["content"].strip()

            if output_format == "json":
                return json.dumps({"suggestions": suggestions}, indent=4)
            return suggestions

        except Exception as e:
            return f"Error occurred while processing: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Debug Sentinel: Analyze Python stack traces and suggest fixes.")
    parser.add_argument("input", help="Path to the file containing the Python stack trace.")
    parser.add_argument("--output-format", choices=["text", "json"], default="text", help="Output format: 'text' or 'json'.")
    parser.add_argument("--api-key", required=True, help="OpenAI API key.")

    args = parser.parse_args()

    try:
        with open(args.input, "r") as file:
            stack_trace = file.read()

        sentinel = DebugSentinel(api_key=args.api_key)
        suggestions = sentinel.suggest_fix(stack_trace, output_format=args.output_format)
        print(suggestions)

    except FileNotFoundError:
        print(f"Error: File '{args.input}' not found.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()