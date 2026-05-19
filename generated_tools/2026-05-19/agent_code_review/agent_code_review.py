import os
import openai
import click
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import TerminalFormatter

# Helper function to analyze code using OpenAI API
def analyze_code(file_content, api_key):
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert Python code reviewer."},
                {"role": "user", "content": f"Please review the following Python code for style, bugs, and optimization opportunities. Provide feedback as inline comments in GitHub-style format.\n\n{file_content}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        return f"Error during API call: {str(e)}"

# Function to process a single file
def process_file(file_path, api_key):
    if not os.path.exists(file_path):
        return f"File not found: {file_path}"
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        print(f"\nAnalyzing file: {file_path}\n")
        print(highlight(content, PythonLexer(), TerminalFormatter()))
        return analyze_code(content, api_key)
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

# Function to process a folder
def process_folder(folder_path, api_key):
    if not os.path.exists(folder_path):
        return f"Folder not found: {folder_path}"
    if not os.path.isdir(folder_path):
        return f"Path is not a folder: {folder_path}"

    results = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                results[file_path] = process_file(file_path, api_key)
    return results

@click.command()
@click.option('--file', 'file_path', type=click.Path(exists=True), help='Path to a Python file to review.')
@click.option('--folder', 'folder_path', type=click.Path(exists=True), help='Path to a folder containing Python files to review.')
@click.option('--api-key', required=True, help='OpenAI API key.')
@click.option('--output', type=click.Path(), help='Path to save the review comments as a markdown file.')
def main(file_path, folder_path, api_key, output):
    "AI-Powered Code Review Agent"
    if not file_path and not folder_path:
        click.echo("Error: You must provide either --file or --folder.")
        return

    if file_path:
        result = process_file(file_path, api_key)
        if output:
            with open(output, 'w') as f:
                f.write(result)
        else:
            click.echo(result)

    if folder_path:
        results = process_folder(folder_path, api_key)
        if output:
            with open(output, 'w') as f:
                for file, review in results.items():
                    f.write(f"# Review for {file}\n\n{review}\n\n")
        else:
            for file, review in results.items():
                click.echo(f"# Review for {file}\n\n{review}\n")

if __name__ == "__main__":
    main()
