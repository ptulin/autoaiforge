import os
import click
from rich.console import Console
from rich.markdown import Markdown

def analyze_code(file_content, style=True, logic=True, bugs=True):
    """
    Analyze the given Python code using OpenAI's API.

    Args:
        file_content (str): The content of the Python file to analyze.
        style (bool): Whether to analyze code style.
        logic (bool): Whether to analyze code logic.
        bugs (bool): Whether to detect potential bugs.

    Returns:
        str: The AI-generated code review report.
    """
    prompt = """
    You are an AI code reviewer. Analyze the following Python code and provide feedback on the following aspects:
    - Style: Suggest improvements to make the code more Pythonic and readable.
    - Logic: Identify any logical issues or inefficiencies.
    - Bugs: Highlight any potential bugs or errors.

    Code:
    ```python
    {code}
    ```

    Provide detailed feedback in markdown format.
    """.format(code=file_content)

    # Mock OpenAI API call for demonstration purposes
    # Replace this with actual OpenAI API call in production
    response = {
        "choices": [
            {
                "text": "### Code Review\n\n#### Style\n- Consider using list comprehensions for better readability.\n\n#### Logic\n- The loop on line 10 could be optimized.\n\n#### Bugs\n- Potential division by zero on line 15."
            }
        ]
    }

    return response["choices"][0]["text"]

@click.command()
@click.option('--files', '-f', multiple=True, required=True, help='One or more Python file paths to review.')
@click.option('--style', is_flag=True, default=True, help='Include style analysis in the review.')
@click.option('--logic', is_flag=True, default=True, help='Include logic analysis in the review.')
@click.option('--bugs', is_flag=True, default=True, help='Include bug detection in the review.')
@click.option('--output', '-o', type=click.Path(), help='Optional output file to save the review as markdown.')
def main(files, style, logic, bugs, output):
    """
    Main function to handle CLI inputs and perform code review.

    Args:
        files (tuple): Paths to Python files to review.
        style (bool): Whether to analyze code style.
        logic (bool): Whether to analyze code logic.
        bugs (bool): Whether to detect potential bugs.
        output (str): Optional file path to save the review.
    """
    console = Console()

    for file_path in files:
        if not os.path.isfile(file_path):
            console.print(f"[bold red]Error:[/bold red] File not found: {file_path}")
            continue

        try:
            with open(file_path, 'r') as file:
                file_content = file.read()

            review = analyze_code(file_content, style, logic, bugs)
            console.print(review)

            if output:
                with open(output, 'w') as out_file:
                    out_file.write(review)
                console.print(f"[bold green]Review saved to {output}[/bold green]")

        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] Failed to analyze {file_path}. {str(e)}")

if __name__ == "__main__":
    main()
