import json
import sys
import click
import openai

def fetch_completions(code_snippet, model):
    """
    Fetch code completions from the OpenAI API.

    Args:
        code_snippet (str): The code snippet to complete.
        model (str): The AI model to use for completion.

    Returns:
        list: A list of completion suggestions.
    """
    try:
        response = openai.Completion.create(
            model=model,
            prompt=code_snippet,
            max_tokens=100,
            n=3,
            stop=None,
            temperature=0.7
        )
        completions = [choice['text'].strip() for choice in response['choices']]
        return completions
    except Exception as e:
        raise RuntimeError(f"Error fetching completions: {e}")

@click.command()
@click.option('--model', default='text-davinci-003', help='AI model to use for code completion.')
@click.option('--output-format', default='json', type=click.Choice(['json', 'text'], case_sensitive=False),
              help='Output format for completions.')
def main(model, output_format):
    """
    Main CLI entry point for the AI Autocomplete CLI tool.

    Args:
        model (str): The AI model to use for completion.
        output_format (str): The output format for completions.
    """
    try:
        # Read code snippet from stdin
        if sys.stdin.isatty():
            click.echo("No input detected. Please pipe a code snippet or provide input via stdin.", err=True)
            sys.exit(1)

        code_snippet = sys.stdin.read().strip()

        if not code_snippet:
            click.echo("Input code snippet is empty.", err=True)
            sys.exit(1)

        completions = fetch_completions(code_snippet, model)

        if output_format == 'json':
            click.echo(json.dumps({"completions": completions}, indent=2))
        else:
            click.echo("\n".join(completions))

    except RuntimeError as e:
        click.echo(str(e), err=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
