import argparse
import openai
import os
from jinja2 import Template
import sys

def fetch_ai_review(file_content, api_key):
    """
    Fetch code review feedback from OpenAI's API.

    Args:
        file_content (str): The content of the code file.
        api_key (str): OpenAI API key.

    Returns:
        str: AI review feedback.
    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a code reviewer."},
                {"role": "user", "content": f"Please review the following code:\n{file_content}"}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        raise RuntimeError(f"Failed to fetch AI review: {e}")

def generate_report(feedback, output_format):
    """
    Generate a report based on AI feedback.

    Args:
        feedback (str): AI feedback text.
        output_format (str): Format of the output report ('markdown' or 'html').

    Returns:
        str: The formatted report.
    """
    template_str = """
    {% if format == 'markdown' %}
    # AI Code Review Report

    {{ feedback }}
    {% elif format == 'html' %}
    <html>
    <head><title>AI Code Review Report</title></head>
    <body>
        <h1>AI Code Review Report</h1>
        <pre>{{ feedback }}</pre>
    </body>
    </html>
    {% endif %}
    """
    template = Template(template_str)
    return template.render(feedback=feedback, format=output_format)

def main():
    parser = argparse.ArgumentParser(description="AI Code Review Reporter")
    parser.add_argument('--file', required=True, help="Path to the code file to review.")
    parser.add_argument('--output', required=True, help="Path to save the generated report.")
    parser.add_argument('--format', choices=['markdown', 'html'], default='markdown', help="Output format of the report.")
    parser.add_argument('--api_key', required=True, help="OpenAI API key.")

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print(f"Error: File {args.file} does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, 'r') as f:
            file_content = f.read()

        if not file_content.strip():
            print("Error: The file is empty.", file=sys.stderr)
            sys.exit(1)

        feedback = fetch_ai_review(file_content, args.api_key)
        report = generate_report(feedback, args.format)

        with open(args.output, 'w') as f:
            f.write(report)

        print(f"Report successfully generated at {args.output}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
