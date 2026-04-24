import os
import argparse
import openai
from graphviz import Digraph

def generate_diagram_from_code(code: str, output_format: str, api_key: str) -> str:
    """
    Generate a diagram from the given code using OpenAI's GPT-5.5 and Graphviz.

    Args:
        code (str): The code snippet or file content to analyze.
        output_format (str): The desired output format (png, svg, or dot).
        api_key (str): OpenAI API key.

    Returns:
        str: The filename of the generated diagram.
    """
    if not code.strip():
        raise ValueError("Code input cannot be empty.")

    if output_format not in ["png", "svg", "dot"]:
        raise ValueError("Invalid output format. Supported formats are: png, svg, dot.")

    openai.api_key = api_key

    try:
        # Use OpenAI GPT-5.5 to generate a description of the code's logic
        response = openai.ChatCompletion.create(
            model="gpt-4.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that converts code into flowchart descriptions."},
                {"role": "user", "content": f"Convert the following code into a flowchart description:\n{code}"}
            ]
        )
        diagram_description = response['choices'][0]['message']['content']

        if not diagram_description.strip():
            raise RuntimeError("Error generating diagram description: Empty response from OpenAI API")

    except Exception as e:
        raise RuntimeError(f"Error generating diagram description: {e}")

    # Create a Graphviz Digraph from the description
    dot = Digraph(format=output_format)
    for line in diagram_description.splitlines():
        parts = line.split("->")
        if len(parts) == 2:
            dot.edge(parts[0].strip(), parts[1].strip())
        elif len(parts) == 1 and parts[0].strip():
            dot.node(parts[0].strip())

    # Save the diagram to a file
    output_file = f"diagram.{output_format}"
    dot.render(output_file, cleanup=True)
    return output_file

def main():
    parser = argparse.ArgumentParser(description="Code-to-Diagram Converter")
    parser.add_argument("--code", required=True, help="Path to the code file or code snippet as a string.")
    parser.add_argument("--output", required=True, help="Output diagram file (e.g., diagram.png, diagram.svg, diagram.dot).")
    parser.add_argument("--api-key", required=True, help="OpenAI API key.")

    args = parser.parse_args()

    # Read the code from the file if a file path is provided
    if os.path.isfile(args.code):
        with open(args.code, "r") as f:
            code = f.read()
    else:
        code = args.code

    # Determine output format from the file extension
    output_format = args.output.split(".")[-1]
    if output_format not in ["png", "svg", "dot"]:
        raise ValueError("Invalid output format. Supported formats are: png, svg, dot.")

    try:
        output_file = generate_diagram_from_code(code, output_format, args.api_key)
        print(f"Diagram generated and saved to {output_file}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
