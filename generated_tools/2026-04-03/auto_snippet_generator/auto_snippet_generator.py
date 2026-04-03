import openai
import click
import os
import sys

def generate_code_snippet(prompt, framework=None):
    """
    Generate a Python code snippet based on a natural language prompt.

    Args:
        prompt (str): The description of the task.
        framework (str, optional): Specific library or framework to use in the snippet.

    Returns:
        str: Generated Python code snippet.
    """
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")

        full_prompt = prompt
        if framework:
            full_prompt += f" using {framework}"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate a Python code snippet for the following task: {full_prompt}. The code should be clean, well-commented, and optimized.",
            max_tokens=150,
            temperature=0.7
        )

        return response.choices[0].text.strip()

    except openai.error.OpenAIError as e:
        raise RuntimeError(f"Error communicating with OpenAI API: {e}")

@click.command()
@click.option('--prompt', required=True, help='Description of the task for which to generate a code snippet.')
@click.option('--framework', default=None, help='Optional framework or library to use in the code snippet.')
@click.option('--output', default=None, help='Optional file path to save the generated code snippet.')
def main(prompt, framework, output):
    """
    Main function to handle CLI arguments and generate the code snippet.

    Args:
        prompt (str): Description of the task.
        framework (str): Optional framework to use.
        output (str): Optional file path to save the snippet.
    """
    try:
        snippet = generate_code_snippet(prompt, framework)

        if output:
            with open(output, 'w') as file:
                file.write(snippet)
            click.echo(f"Code snippet saved to {output}")
        else:
            click.echo("Generated Code Snippet:")
            click.echo(snippet)

    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
