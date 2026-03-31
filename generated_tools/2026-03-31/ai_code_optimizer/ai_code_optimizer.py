import os
import click
import openai
import anthropic

def analyze_code_with_gpt(code, api_key):
    """Analyze code using OpenAI's GPT model."""
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following Python code for performance, readability, and maintainability improvements:\n\n{code}\n\nProvide detailed suggestions:",
            max_tokens=500
        )
        return response.choices[0].text.strip()
    except openai.error.OpenAIError as e:
        return f"Error analyzing code with GPT: {e}"

def analyze_code_with_claude(code, api_key):
    """Analyze code using Anthropic's Claude model."""
    client = anthropic.Client(api_key)
    try:
        response = client.completion(
            prompt=f"\n\nHuman: Analyze the following Python code for performance, readability, and maintainability improvements:\n\n{code}\n\nProvide detailed suggestions.\n\nAssistant:",
            model="claude-v1",
            max_tokens_to_sample=500
        )
        return response["completion"].strip()
    except Exception as e:
        return f"Error analyzing code with Claude: {e}"

def annotate_code(file_path, gpt_key, claude_key):
    """Read a Python script, analyze it with GPT and Claude, and return annotated suggestions."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, "r") as f:
        code = f.read()

    if not code.strip():
        return "The file is empty. No code to analyze."

    gpt_suggestions = analyze_code_with_gpt(code, gpt_key)
    claude_suggestions = analyze_code_with_claude(code, claude_key)

    return f"GPT Suggestions:\n{gpt_suggestions}\n\nClaude Suggestions:\n{claude_suggestions}"

@click.command()
@click.option('--file', 'file_path', required=True, type=click.Path(exists=True), help='Path to the Python script file to analyze.')
@click.option('--gpt-key', required=True, help='OpenAI API key for GPT.')
@click.option('--claude-key', required=True, help='Anthropic API key for Claude.')
def main(file_path, gpt_key, claude_key):
    """AI Code Optimizer CLI entry point."""
    try:
        result = annotate_code(file_path, gpt_key, claude_key)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error: {e}")

if __name__ == "__main__":
    main()
