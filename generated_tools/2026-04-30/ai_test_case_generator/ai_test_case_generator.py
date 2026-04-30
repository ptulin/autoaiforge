import os
import openai
import click

def generate_test_cases(api_key, file_path, function_name=None):
    """
    Generate pytest test cases for a given Python file or function.

    Args:
        api_key (str): OpenAI API key.
        file_path (str): Path to the Python file.
        function_name (str, optional): Specific function to generate tests for. Defaults to None.

    Returns:
        str: Generated pytest test cases as a string.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    with open(file_path, 'r') as file:
        code_content = file.read()

    prompt = f"""
    You are an expert Python developer. Generate pytest test cases for the following Python code.
    Include parameterized tests where applicable and add comments explaining each test case.

    Code:
    {code_content}

    """
    if function_name:
        prompt += f"Focus on the function named '{function_name}'."

    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )
        return response["choices"][0]["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Failed to generate test cases: {e}")

@click.command()
@click.option('--file', 'file_path', required=True, type=click.Path(exists=True), help="Path to the Python file.")
@click.option('--function', 'function_name', required=False, help="Specific function to generate tests for.")
@click.option('--output', 'output_file', required=True, type=click.Path(), help="Path to save the generated test file.")
@click.option('--api-key', 'api_key', envvar='OPENAI_API_KEY', required=True, help="OpenAI API key.")
def main(file_path, function_name, output_file, api_key):
    """
    CLI entry point for the AI Test Case Generator.
    """
    try:
        test_cases = generate_test_cases(api_key, file_path, function_name)
        with open(output_file, 'w') as f:
            f.write(test_cases)
        click.echo(f"Test cases generated and saved to {output_file}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    main()
