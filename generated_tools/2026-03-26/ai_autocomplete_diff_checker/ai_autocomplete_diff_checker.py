import argparse
import difflib

def generate_diff(original_file, suggested_file, output_file):
    """
    Generate a unified diff between the original file and the AI-suggested file.

    Args:
        original_file (str): Path to the original source file.
        suggested_file (str): Path to the AI-suggested modified file.
        output_file (str): Path to save the generated diff file.

    Returns:
        str: The generated diff as a string.
    """
    try:
        with open(original_file, 'r') as orig:
            original_lines = orig.readlines()

        with open(suggested_file, 'r') as sugg:
            suggested_lines = sugg.readlines()

        diff = difflib.unified_diff(
            original_lines,
            suggested_lines,
            fromfile=original_file,
            tofile=suggested_file,
            lineterm=''
        )

        diff_output = '\n'.join(diff)

        if output_file:
            with open(output_file, 'w') as output:
                output.write(diff_output)

        return diff_output

    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {e.filename}")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="AI Autocomplete Diff Checker: Compare original and AI-suggested code files."
    )
    parser.add_argument(
        'original_file',
        type=str,
        help="Path to the original source file."
    )
    parser.add_argument(
        'suggested_file',
        type=str,
        help="Path to the AI-suggested modified file."
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help="Path to save the generated diff file (optional)."
    )

    args = parser.parse_args()

    try:
        diff_output = generate_diff(args.original_file, args.suggested_file, args.output)
        print("Diff generated successfully.")
        if not args.output:
            print(diff_output)
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except RuntimeError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()