import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from jinja2 import Template
import os
import argparse

def generate_report(predictions, metadata=None, output_format='json', output_path='report'):
    """
    Generate a diagnostic report based on predictions and metadata.

    Args:
        predictions (dict): Model predictions, e.g., {'tumor_probability': 0.85}.
        metadata (dict, optional): Additional metadata, e.g., patient info.
        output_format (str): 'json' or 'pdf'.
        output_path (str): Path to save the output file (without extension).

    Returns:
        str: Path to the generated report.
    """
    if not predictions or not isinstance(predictions, dict):
        raise ValueError("Predictions must be a non-empty dictionary.")

    if metadata and not isinstance(metadata, dict):
        raise ValueError("Metadata must be a dictionary if provided.")

    report_data = {
        "predictions": predictions,
        "metadata": metadata or {},
    }

    if output_format == 'json':
        output_file = f"{output_path}.json"
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=4)
        return output_file

    elif output_format == 'pdf':
        output_file = f"{output_path}.pdf"
        generate_pdf_report(report_data, output_file)
        return output_file

    else:
        raise ValueError("Unsupported output format. Use 'json' or 'pdf'.")

def generate_pdf_report(report_data, output_file):
    """
    Generate a PDF report using ReportLab.

    Args:
        report_data (dict): Data to include in the report.
        output_file (str): Path to save the PDF file.
    """
    c = canvas.Canvas(output_file, pagesize=letter)
    c.setFont("Helvetica", 12)

    y_position = 750
    c.drawString(50, y_position, "AI Diagnostic Report")
    y_position -= 20

    for key, value in report_data["predictions"].items():
        c.drawString(50, y_position, f"{key}: {value}")
        y_position -= 20

    if report_data["metadata"]:
        c.drawString(50, y_position, "Metadata:")
        y_position -= 20
        for key, value in report_data["metadata"].items():
            c.drawString(70, y_position, f"{key}: {value}")
            y_position -= 20

    c.save()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AI Diagnostic Report Generator")
    parser.add_argument("--predictions", type=str, required=True, help="Path to JSON file with predictions.")
    parser.add_argument("--metadata", type=str, help="Path to JSON file with metadata.")
    parser.add_argument("--output_format", type=str, choices=['json', 'pdf'], default='json', help="Output format.")
    parser.add_argument("--output_path", type=str, default='report', help="Output file path (without extension).")

    args = parser.parse_args()

    with open(args.predictions, 'r') as f:
        predictions = json.load(f)

    metadata = None
    if args.metadata:
        with open(args.metadata, 'r') as f:
            metadata = json.load(f)

    output_file = generate_report(predictions, metadata, args.output_format, args.output_path)
    print(f"Report generated: {output_file}")