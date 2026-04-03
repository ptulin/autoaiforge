import os
import click
import openai
import black

def refactor_code(file_path, output_path, rename_vars, restructure_code, optimize_performance):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as f:
        original_code = f.read()

    # Prepare the prompt for the AI model
    prompt = f"""
    Refactor the following Python code based on the specified options:
    - Rename variables: {rename_vars}
    - Restructure code for readability: {restructure_code}
    - Optimize performance: {optimize_performance}

    Code:
    {original_code}
    """

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500
        )
        refactored_code = response["choices"][0]["text"].strip()
    except Exception as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

    # Format the code using Black
    try:
        refactored_code = black.format_str(refactored_code, mode=black.FileMode())
    except black.InvalidInput as e:
        raise ValueError(f"Error formatting code with Black: {e}")

    # Save the refactored code to the output file
    with open(output_path, 'w') as f:
        f.write(refactored_code)

@click.command()
@click.option('--file', 'file_path', required=True, type=click.Path(exists=True), help="Path to the Python file to refactor.")
@click.option('--output', 'output_path', required=True, type=click.Path(), help="Path to save the refactored Python file.")
@click.option('--rename-vars', is_flag=True, help="Enable renaming of variables and functions.")
@click.option('--restructure-code', is_flag=True, help="Enable restructuring of code for better readability.")
@click.option('--optimize-performance', is_flag=True, help="Enable performance optimization.")
def main(file_path, output_path, rename_vars, restructure_code, optimize_performance):
    """AI Code Refactor: Refactor Python code using AI."""
    try:
        refactor_code(file_path, output_path, rename_vars, restructure_code, optimize_performance)
        click.echo(f"Refactored code saved to {output_path}")
    except Exception as e:
        click.echo(f"Error: {e}", err=True)

if __name__ == "__main__":
    main()
