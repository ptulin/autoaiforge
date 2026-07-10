import os
import click
import openai
from diff_match_patch import diff_match_patch

def analyze_code_with_ai(code):
    """
    Uses OpenAI's API to analyze code for vulnerabilities and suggest fixes.

    Args:
        code (str): The source code to analyze.

    Returns:
        tuple: A tuple containing the analysis and the sanitized code.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI that reviews code for security vulnerabilities and suggests fixes."},
                {"role": "user", "content": f"Analyze this code for vulnerabilities and suggest fixes:\n{code}"}
            ]
        )
        analysis = response['choices'][0]['message']['content']
        sanitized_code = extract_sanitized_code(analysis)
        return analysis, sanitized_code
    except Exception as e:
        raise RuntimeError(f"Failed to analyze code with AI: {e}")

def extract_sanitized_code(analysis):
    """
    Extracts the sanitized code from the AI's response.

    Args:
        analysis (str): The analysis response from the AI.

    Returns:
        str: The sanitized code extracted from the analysis.
    """
    # Assuming the AI returns the sanitized code in a block marked by triple backticks
    if "```" in analysis:
        parts = analysis.split("```")
        if len(parts) > 1:
            return parts[1].strip()
    return ""  # Return empty string if no sanitized code is found

def process_file(file_path, sanitize):
    """
    Processes a single file for vulnerabilities and optionally sanitizes it.

    Args:
        file_path (str): Path to the file to process.
        sanitize (bool): Whether to generate a sanitized version of the file.

    Returns:
        str: The processed file content with annotations or sanitized code.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        code = f.read()

    analysis, sanitized_code = analyze_code_with_ai(code)

    if sanitize:
        return sanitized_code
    else:
        return f"# Analysis:\n{analysis}\n\n# Original Code:\n{code}"

def process_directory(directory_path, sanitize):
    """
    Processes all files in a directory for vulnerabilities and optionally sanitizes them.

    Args:
        directory_path (str): Path to the directory to process.
        sanitize (bool): Whether to generate sanitized versions of the files.

    Returns:
        dict: A dictionary with file paths as keys and processed content as values.
    """
    if not os.path.isdir(directory_path):
        raise NotADirectoryError(f"Directory not found: {directory_path}")

    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r') as f:
                    code = f.read()
                analysis, sanitized_code = analyze_code_with_ai(code)
                results[file_path] = sanitized_code if sanitize else f"# Analysis:\n{analysis}\n\n# Original Code:\n{code}"
            except Exception as e:
                results[file_path] = f"Error processing file: {e}"

    return results

@click.command()
@click.option('--file', 'file_path', type=click.Path(exists=True), help='Path to the source code file.')
@click.option('--directory', 'directory_path', type=click.Path(exists=True), help='Path to the source code directory.')
@click.option('--sanitize', is_flag=True, help='Generate sanitized code.')
def main(file_path, directory_path, sanitize):
    """
    Main entry point for the AI-Powered Code Sanitizer CLI tool.
    """
    if not file_path and not directory_path:
        raise click.UsageError("You must provide either --file or --directory.")

    if file_path:
        try:
            result = process_file(file_path, sanitize)
            click.echo(result)
        except Exception as e:
            click.echo(f"Error: {e}")

    if directory_path:
        try:
            results = process_directory(directory_path, sanitize)
            for file_path, content in results.items():
                click.echo(f"{file_path}:\n{content}\n")
        except Exception as e:
            click.echo(f"Error: {e}")

if __name__ == "__main__":
    main()
