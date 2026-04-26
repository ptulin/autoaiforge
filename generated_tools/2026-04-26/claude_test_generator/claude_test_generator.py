import os
import openai
import click

def generate_tests_with_claude(api_key, code_snippet):
    """
    Generate unit tests for the given Python code snippet using Claude AI.

    Args:
        api_key (str): OpenAI API key for Claude.
        code_snippet (str): Python code snippet to analyze.

    Returns:
        str: Generated unit test code.
    """
    openai.api_key = api_key

    prompt = (
        "You are an AI that generates Python unit tests. "
        "Given the following Python code, write unit tests using pytest to cover its functionality. "
        "Include edge cases and error handling scenarios.\n\n"
        f"Code:\n{code_snippet}\n\n"
        "Unit Tests:"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error communicating with Claude AI: {e}")

@click.command()
@click.option('--input', 'input_path', required=True, type=click.Path(exists=True), help="Path to the Python file to analyze.")
@click.option('--output', 'output_path', required=True, type=click.Path(), help="Path to save the generated test file.")
@click.option('--api-key', 'api_key', required=True, help="OpenAI API key for Claude.")
def main(input_path, output_path, api_key):
    """
    CLI entry point for the Claude Test Generator.

    Args:
        input_path (str): Path to the Python file to analyze.
        output_path (str): Path to save the generated test file.
        api_key (str): OpenAI API key for Claude.
    """
    try:
        with open(input_path, 'r') as f:
            code_snippet = f.read()

        generated_tests = generate_tests_with_claude(api_key, code_snippet)

        with open(output_path, 'w') as f:
            f.write(generated_tests)

        click.echo(f"Test cases generated and saved to {output_path}")
    except FileNotFoundError:
        click.echo("Error: Input file not found.", err=True)
    except RuntimeError as e:
        click.echo(f"Error: {e}", err=True)
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}", err=True)

if __name__ == "__main__":
    main()
