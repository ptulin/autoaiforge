import argparse
import traceback
import os
import openai

def parse_error_log(error_log):
    """
    Parses the error log and extracts key details such as error type, message, and stack trace.

    Args:
        error_log (str): The error log content.

    Returns:
        dict: A dictionary containing extracted error details.
    """
    try:
        stack_lines = error_log.strip().split('\n')
        last_line = stack_lines[-1] if stack_lines else ""
        error_type, _, error_message = last_line.partition(":")
        return {
            "error_type": error_type.strip(),
            "error_message": error_message.strip(),
            "stack_trace": stack_lines
        }
    except Exception as e:
        raise ValueError("Failed to parse error log: " + str(e))

def generate_debug_prompt(error_details):
    """
    Generates a debugging prompt for AI coding assistants based on error details.

    Args:
        error_details (dict): A dictionary containing error details.

    Returns:
        str: A debugging prompt tailored to the error.
    """
    try:
        prompt = (
            f"I encountered an error in my code. The error type is '{error_details['error_type']}' "
            f"with the message: '{error_details['error_message']}'. Here is the stack trace: \n"
            f"{os.linesep.join(error_details['stack_trace'])}\n"
            "Can you help me understand what might be causing this issue and how to resolve it?"
        )
        return prompt
    except KeyError as e:
        raise ValueError("Missing key in error details: " + str(e))

def main():
    parser = argparse.ArgumentParser(description="AI Debug Prompt Generator")
    parser.add_argument('--error-log', type=str, required=True, help="Path to the error log file")
    args = parser.parse_args()

    try:
        if not os.path.exists(args.error_log):
            raise FileNotFoundError(f"The file '{args.error_log}' does not exist.")

        with open(args.error_log, 'r') as file:
            error_log_content = file.read()

        error_details = parse_error_log(error_log_content)
        prompt = generate_debug_prompt(error_details)

        print("Generated Debugging Prompt:")
        print(prompt)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()