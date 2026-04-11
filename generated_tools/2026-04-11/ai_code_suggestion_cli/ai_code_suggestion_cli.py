import click
import openai
import os

@click.command()
@click.option('--language', required=True, help='The programming language for the code suggestion.')
@click.option('--snippet', required=True, help='The incomplete code snippet or function signature.')
@click.option('--comment', default='', help='Optional comment or description to guide the AI.')
@click.option('--output', default=None, help='Optional file path to save the generated code.')
def ai_code_suggestion_cli(language, snippet, comment, output):
    """
    CLI tool to provide AI-powered code suggestions based on input.
    """
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        click.echo('Error: OPENAI_API_KEY environment variable is not set.', err=True)
        return

    openai.api_key = openai_api_key

    prompt = f"Language: {language}\nSnippet: {snippet}\nComment: {comment}\n\nGenerate the complete code with explanation."

    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        generated_code = response.choices[0].text.strip()

        if output:
            try:
                with open(output, 'w') as f:
                    f.write(generated_code)
                click.echo(f'Code suggestion saved to {output}')
            except IOError as e:
                click.echo(f'Error: Unable to write to file {output}. {str(e)}', err=True)
        else:
            click.echo('Generated Code:')
            click.echo(generated_code)

    except openai.error.OpenAIError as e:
        click.echo(f'Error: {str(e)}', err=True)
        return
    except Exception as e:
        click.echo(f'Unexpected error: {str(e)}', err=True)
        return

if __name__ == '__main__':
    ai_code_suggestion_cli()
