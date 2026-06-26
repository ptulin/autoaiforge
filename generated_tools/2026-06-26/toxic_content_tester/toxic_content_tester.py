import argparse
import json
import pandas as pd
import os
from io import StringIO

def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Error loading CSV file: {e}")

def load_json(file_path):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Error loading JSON file: {e}")

def evaluate_outputs(outputs, rules):
    results = []
    for index, output in outputs.iterrows():
        flagged_rules = []
        for rule in rules:
            if rule['keyword'].lower() in output['content'].lower():
                flagged_rules.append(rule['description'])
        results.append({
            'id': output['id'],
            'content': output['content'],
            'flagged_rules': flagged_rules
        })
    return results

def generate_report(results, report_path, format):
    if format == 'json':
        with open(report_path, 'w') as f:
            json.dump(results, f, indent=4)
    elif format == 'html':
        html_content = "<html><body><h1>Safety Audit Report</h1><table border='1'>"
        html_content += "<tr><th>ID</th><th>Content</th><th>Flagged Rules</th></tr>"
        for result in results:
            html_content += f"<tr><td>{result['id']}</td><td>{result['content']}</td><td>{', '.join(result['flagged_rules'])}</td></tr>"
        html_content += "</table></body></html>"
        with open(report_path, 'w') as f:
            f.write(html_content)
    else:
        raise ValueError("Unsupported report format. Use 'json' or 'html'.")

def main():
    parser = argparse.ArgumentParser(description="Toxic Content Tester")
    parser.add_argument('--outputs', required=True, help="Path to the CSV file containing AI outputs")
    parser.add_argument('--rules', required=True, help="Path to the JSON file containing safety rules")
    parser.add_argument('--report', required=True, help="Path to save the generated report")
    parser.add_argument('--format', choices=['json', 'html'], default='json', help="Format of the report (json or html)")

    args = parser.parse_args()

    try:
        outputs = load_csv(args.outputs)
        rules = load_json(args.rules)
        results = evaluate_outputs(outputs, rules)
        generate_report(results, args.report, args.format)
        print(f"Report generated successfully at {args.report}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()