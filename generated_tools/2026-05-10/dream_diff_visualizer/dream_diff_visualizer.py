import argparse
import difflib
import json
from jinja2 import Template

def load_file(file_path):
    """Load content from a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Error reading file {file_path}: {e}")

def generate_diff(content1, content2):
    """Generate a diff between two strings."""
    differ = difflib.HtmlDiff()
    return differ.make_file(content1.splitlines(), content2.splitlines(), context=True, numlines=0)

def generate_html_diff(file1, file2, output_file):
    """Generate an interactive HTML diff file."""
    content1 = load_file(file1)
    content2 = load_file(file2)

    try:
        # Attempt to parse as JSON for pretty printing
        content1 = json.dumps(json.loads(content1), indent=4)
        content2 = json.dumps(json.loads(content2), indent=4)
    except json.JSONDecodeError:
        pass  # If not JSON, treat as plain text

    diff_html = generate_diff(content1, content2)

    template = Template("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dream Diff Visualizer</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
            .diff { margin: 20px; }
        </style>
    </head>
    <body>
        <h1>Dream Diff Visualizer</h1>
        <div class="diff">
            {{ diff_html|safe }}
        </div>
    </body>
    </html>
    """)

    final_html = template.render(diff_html=diff_html)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)
    except Exception as e:
        raise RuntimeError(f"Error writing to output file {output_file}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Dream Diff Visualizer: Compare two dreaming session outputs and generate an interactive visual diff.")
    parser.add_argument('--file1', required=True, help="Path to the first file")
    parser.add_argument('--file2', required=True, help="Path to the second file")
    parser.add_argument('--output', required=True, help="Path to the output HTML file")

    args = parser.parse_args()

    try:
        generate_html_diff(args.file1, args.file2, args.output)
        print(f"Diff successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
