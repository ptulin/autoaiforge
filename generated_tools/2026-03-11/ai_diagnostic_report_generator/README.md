# AI Diagnostic Report Generator

## Description
The AI Diagnostic Report Generator is a Python library designed to create structured diagnostic reports from AI model outputs. It supports generating reports in both JSON and PDF formats, making it easy to integrate AI predictions into healthcare systems.

## Features
- Generate reports in JSON or PDF format
- Customizable report templates
- Support for multiple diagnostic categories

## Installation
```bash
pip install reportlab==3.6.12 jinja2==3.1.2
```

## Usage
```python
from ai_diagnostic_report_generator import generate_report

predictions = {"tumor_probability": 0.85}
metadata = {"patient_id": "12345", "age": 45, "gender": "female"}

# Generate JSON report
json_report = generate_report(predictions, metadata, output_format='json', output_path='diagnostic_report')
print(f"JSON report saved to: {json_report}")

# Generate PDF report
pdf_report = generate_report(predictions, metadata, output_format='pdf', output_path='diagnostic_report')
print(f"PDF report saved to: {pdf_report}")
```

## CLI Usage
```bash
python ai_diagnostic_report_generator.py --predictions predictions.json --metadata metadata.json --output_format pdf --output_path diagnostic_report
```

## License
This project is licensed under the MIT License.