import ast
import argparse
import pylint.lint
from pylint.reporters import text


def refactor_code(code):
    # Simple refactoring example: remove trailing whitespace
    return code.rstrip()


def main(input_file, output_file):
    # Read input code
    try:
        with open(input_file, 'r') as f:
            code = f.read()
    except FileNotFoundError as e:
        print(f"Error: Input file '{input_file}' not found.")
        raise e

    # Refactor code
    refactored_code = refactor_code(code)

    # Write refactored code to output file
    with open(output_file, 'w') as f:
        f.write(refactored_code)

    # Run pylint on refactored code
    try:
        pylint.lint.Run([output_file], reporter=text.TextReporter(), exit=False)
    except Exception as e:
        print(f"Error running pylint: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Auto Code Refactor Tool')
    parser.add_argument('--input', help='Input code file or directory')
    parser.add_argument('--output', help='Output refactored code file or directory')
    args = parser.parse_args()
    main(args.input, args.output)
