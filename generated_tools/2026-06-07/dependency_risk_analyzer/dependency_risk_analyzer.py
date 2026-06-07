import argparse
import json
import os
import re
from typing import List, Dict
import requests
import pandas as pd
from transformers import pipeline

# Constants
CVE_API_URL = "https://services.nvd.nist.gov/rest/json/cves/1.0"

# Function to parse requirements.txt or pyproject.toml
def parse_dependencies(file_path: str) -> List[Dict[str, str]]:
    dependencies = []
    if file_path.endswith("requirements.txt"):
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    match = re.match(r"([a-zA-Z0-9_\-]+)([=><!~]+[0-9\.]+)?", line)
                    if match:
                        dependencies.append({"name": match.group(1), "version": match.group(2) or "unknown"})
    elif file_path.endswith("pyproject.toml"):
        try:
            import toml
            data = toml.load(file_path)
            deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
            for dep, version in deps.items():
                if isinstance(version, str):
                    dependencies.append({"name": dep, "version": version})
                else:
                    dependencies.append({"name": dep, "version": "unknown"})
        except ImportError:
            raise ImportError("Please install the 'toml' package to parse pyproject.toml files.")
    else:
        raise ValueError("Unsupported file format. Only requirements.txt and pyproject.toml are supported.")
    return dependencies

# Function to query CVE database
def query_cve_database(package_name: str, version: str) -> List[Dict[str, str]]:
    try:
        response = requests.get(CVE_API_URL, params={"keyword": package_name, "resultsPerPage": 5})
        response.raise_for_status()
        cve_data = response.json()
        vulnerabilities = []
        for item in cve_data.get("result", {}).get("CVE_Items", []):
            description = item.get("cve", {}).get("description", {}).get("description_data", [{}])[0].get("value", "")
            vulnerabilities.append({
                "id": item.get("cve", {}).get("CVE_data_meta", {}).get("ID", "unknown"),
                "description": description
            })
        return vulnerabilities
    except requests.RequestException:
        return []

# Function to classify risk using AI model
def classify_risk(vulnerabilities: List[Dict[str, str]]) -> List[Dict[str, str]]:
    classifier = pipeline("text-classification", model="distilbert-base-uncased")
    for vulnerability in vulnerabilities:
        risk_classification = classifier(vulnerability["description"])[0]
        vulnerability["risk_level"] = risk_classification["label"]
        vulnerability["confidence"] = risk_classification["score"]
    return vulnerabilities

# Main function to analyze dependencies
def analyze_dependencies(file_path: str, output_format: str) -> str:
    dependencies = parse_dependencies(file_path)
    results = []
    for dependency in dependencies:
        vulnerabilities = query_cve_database(dependency["name"], dependency["version"])
        classified_vulnerabilities = classify_risk(vulnerabilities)
        results.append({
            "dependency": dependency,
            "vulnerabilities": classified_vulnerabilities
        })

    if output_format == "json":
        return json.dumps(results, indent=4)
    elif output_format == "markdown":
        markdown_report = "# Dependency Risk Report\n\n"
        for result in results:
            markdown_report += f"## {result['dependency']['name']} ({result['dependency']['version']})\n"
            for vuln in result["vulnerabilities"]:
                markdown_report += f"- **{vuln['id']}**: {vuln['description']}\n"
                markdown_report += f"  - Risk Level: {vuln['risk_level']} (Confidence: {vuln['confidence']:.2f})\n"
            markdown_report += "\n"
        return markdown_report
    else:
        raise ValueError("Unsupported output format. Use 'json' or 'markdown'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze Python project dependencies for security vulnerabilities.")
    parser.add_argument("file_path", type=str, help="Path to requirements.txt or pyproject.toml file.")
    parser.add_argument("--output-format", type=str, choices=["json", "markdown"], default="json", help="Output format for the risk report.")
    args = parser.parse_args()

    try:
        report = analyze_dependencies(args.file_path, args.output_format)
        print(report)
    except Exception as e:
        print(f"Error: {e}")