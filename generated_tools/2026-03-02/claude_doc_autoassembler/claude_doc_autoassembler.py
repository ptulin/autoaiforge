import argparse
import json
import csv
from pathlib import Path
from jinja2 import Template
from docx import Document
from fpdf import FPDF
import requests

def load_input_data(input_path):
    """Load input data from a JSON or CSV file."""
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file {input_path} not found.")

    if input_path.suffix == ".json":
        with open(input_path, "r") as f:
            return json.load(f)
    elif input_path.suffix == ".csv":
        with open(input_path, "r") as f:
            reader = csv.DictReader(f)
            return [row for row in reader]
    else:
        raise ValueError("Unsupported input file format. Use JSON or CSV.")

def load_template(template_path):
    """Load a Jinja2 template from a file."""
    template_path = Path(template_path)
    if not template_path.exists():
        raise FileNotFoundError(f"Template file {template_path} not found.")

    with open(template_path, "r") as f:
        return Template(f.read())

def generate_content(template, data):
    """Generate content using the template and input data."""
    return template.render(data)

def refine_with_claude(content, api_key):
    """Refine content using Claude AI API."""
    url = "https://api.anthropic.com/v1/complete"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": content,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise RuntimeError(f"Claude API error: {response.text}")

    return response.json().get("completion", content)

def save_as_pdf(content, output_path):
    """Save content as a PDF file."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, content)
    pdf.output(output_path)

def save_as_docx(content, output_path):
    """Save content as a Word document."""
    doc = Document()
    doc.add_paragraph(content)
    doc.save(output_path)

def main():
    parser = argparse.ArgumentParser(description="Claude Document Auto-Assembler")
    parser.add_argument("--template", required=True, help="Path to the template file (Jinja2 format).")
    parser.add_argument("--input", required=True, help="Path to the input data file (JSON or CSV).")
    parser.add_argument("--output", required=True, help="Path to the output file (PDF or DOCX).")
    parser.add_argument("--api-key", required=True, help="API key for Claude AI.")

    args = parser.parse_args()

    try:
        data = load_input_data(args.input)
        template = load_template(args.template)

        # If input data is a list (e.g., from CSV), process each item separately
        if isinstance(data, list):
            content = "\n".join([generate_content(template, item) for item in data])
        else:
            content = generate_content(template, data)

        refined_content = refine_with_claude(content, args.api_key)

        output_path = Path(args.output)
        if output_path.suffix == ".pdf":
            save_as_pdf(refined_content, output_path)
        elif output_path.suffix == ".docx":
            save_as_docx(refined_content, output_path)
        else:
            raise ValueError("Unsupported output file format. Use PDF or DOCX.")

        print(f"Document generated and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()