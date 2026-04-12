import os
import click
import openai

def analyze_code(file_content):
    """
    Uses OpenAI API to analyze Python code for bugs, optimizations, and best practices.

    Args:
        file_content (str): The content of the Python file to analyze.

    Returns:
        str: The analysis report from OpenAI.
    """
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Analyze the following Python code for bugs, optimizations, and best practices:\n\n{file_content}\n\nProvide a detailed report:",
            max_tokens=1000
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        return f"Error during analysis: {str(e)}"

def process_file(file_path):
    """
    Reads a Python file and analyzes its content.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        str: Analysis report for the file.
    """
    if not os.path.isfile(file_path):
        return f"Error: File not found - {file_path}"

    if not file_path.endswith('.py'):
        return f"Error: File is not a Python script - {file_path}"

    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return analyze_code(content)
    except Exception as e:
        return f"Error reading file {file_path}: {str(e)}"

def process_directory(directory_path):
    """
    Analyzes all Python files in a directory.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        dict: A dictionary mapping file names to their analysis reports.
    """
    if not os.path.isdir(directory_path):
        return {"error": f"Directory not found - {directory_path}"}

    reports = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                reports[file_path] = process_file(file_path)

    return reports

@click.command()
@click.option('--file', 'file_path', type=click.Path(exists=True), help='Path to a Python file to analyze.')
@click.option('--directory', 'directory_path', type=click.Path(exists=True), help='Path to a directory containing Python files to analyze.')
@click.option('--output', 'output_path', type=click.Path(), help='Path to save the analysis report.')
def main(file_path, directory_path, output_path):
    """
    CLI entry point for the AI-Powered Code Review tool.
    """
    if not file_path and not directory_path:
        click.echo("Error: You must provide either --file or --directory.")
        return

    if file_path:
        report = process_file(file_path)
    elif directory_path:
        report = process_directory(directory_path)

    if output_path:
        try:
            with open(output_path, 'w') as output_file:
                if isinstance(report, dict):
                    for file, analysis in report.items():
                        output_file.write(f"File: {file}\n{analysis}\n\n")
                else:
                    output_file.write(report)
            click.echo(f"Analysis report saved to {output_path}")
        except Exception as e:
            click.echo(f"Error saving report: {str(e)}")
    else:
        if isinstance(report, dict):
            for file, analysis in report.items():
                click.echo(f"File: {file}\n{analysis}\n")
        else:
            click.echo(report)

if __name__ == "__main__":
    main()
