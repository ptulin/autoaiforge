import openai
import click
import yaml
import sys

# Function to interact with OpenAI API
def get_debugging_suggestions(input_text):
    """
    Sends the input text to OpenAI's API and retrieves debugging suggestions.

    Args:
        input_text (str): The error message, stack trace, or problematic code.

    Returns:
        dict: A dictionary containing debugging suggestions and explanations.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for debugging Python code."},
                {"role": "user", "content": input_text}
            ]
        )
        suggestions = response['choices'][0]['message']['content']
        return {"suggestions": suggestions}
    except Exception as e:
        return {"error": str(e)}

@click.command()
@click.option('--input', 'input_file', type=click.File('r'), required=False, help='Path to the input file containing error message, stack trace, or code.')
@click.option('--output', 'output_file', type=click.File('w'), required=False, help='Path to the output YAML file to save suggestions.')
def main(input_file, output_file):
    """
    Code Debug AI Assistant CLI tool.

    Takes error messages, stack traces, or problematic code as input and uses OpenAI to suggest debugging steps or fixes.
    """
    # Read input from file or stdin
    if input_file:
        input_text = input_file.read()
    else:
        click.echo("Enter your error message, stack trace, or problematic code (end with Ctrl+D):")
        input_text = sys.stdin.read()

    if not input_text.strip():
        click.echo("Error: No input provided.", err=True)
        sys.exit(1)

    # Get debugging suggestions
    result = get_debugging_suggestions(input_text)

    # Handle errors from the API
    if "error" in result:
        click.echo(f"Error communicating with OpenAI API: {result['error']}", err=True)
        sys.exit(1)

    # Output results
    if output_file:
        yaml.dump(result, output_file)
        click.echo(f"Suggestions saved to {output_file.name}")
    else:
        click.echo("Debugging Suggestions:")
        click.echo(result["suggestions"])

if __name__ == "__main__":
    main()
