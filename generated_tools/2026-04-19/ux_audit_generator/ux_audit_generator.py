import argparse
import json
import os
import requests
from jinja2 import Template

def fetch_audit_results(api_url, api_key, prototype_data, description):
    """
    Fetches audit results from the Claude Design API.

    :param api_url: URL of the Claude Design API
    :param api_key: API key for authentication
    :param prototype_data: JSON data of the prototype
    :param description: Optional text description of the prototype
    :return: Audit results as a dictionary
    """
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"prototype_data": prototype_data, "description": description}

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error fetching audit results: {e}")

def generate_report(audit_results, output_format):
    """
    Generates an audit report in the specified format.

    :param audit_results: Audit results as a dictionary
    :param output_format: Either 'html' or 'md'
    :return: Rendered report as a string
    """
    template_str = """
    {% if output_format == 'html' %}
    <html>
    <head><title>UX Audit Report</title></head>
    <body>
        <h1>UX Audit Report</h1>
        <h2>Summary</h2>
        <p>{{ audit_results.summary }}</p>
        <h2>Details</h2>
        <ul>
        {% for issue in audit_results.issues %}
            <li><strong>{{ issue.title }}</strong>: {{ issue.description }}</li>
        {% endfor %}
        </ul>
    </body>
    </html>
    {% else %}
    # UX Audit Report

    ## Summary
    {{ audit_results.summary }}

    ## Details
    {% for issue in audit_results.issues %}
    - **{{ issue.title }}**: {{ issue.description }}
    {% endfor %}
    {% endif %}
    """
    template = Template(template_str)
    return template.render(audit_results=audit_results, output_format=output_format)

def main():
    parser = argparse.ArgumentParser(description="UX Audit Generator")
    parser.add_argument("--input", required=True, help="Path to the prototype JSON file")
    parser.add_argument("--output", required=True, help="Path to save the generated report")
    parser.add_argument("--api-url", required=True, help="Claude Design API URL")
    parser.add_argument("--api-key", required=True, help="Claude Design API Key")
    parser.add_argument("--description", help="Optional text description of the prototype")
    parser.add_argument("--format", choices=["html", "md"], default="md", help="Output format (html or md)")

    args = parser.parse_args()

    # Load prototype data
    if not os.path.exists(args.input):
        raise FileNotFoundError(f"Input file {args.input} does not exist.")

    with open(args.input, "r") as f:
        try:
            prototype_data = json.load(f)
        except json.JSONDecodeError:
            raise ValueError("Input file is not valid JSON.")

    # Fetch audit results
    audit_results = fetch_audit_results(args.api_url, args.api_key, prototype_data, args.description)

    # Generate report
    report = generate_report(audit_results, args.format)

    # Save report to file
    with open(args.output, "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()