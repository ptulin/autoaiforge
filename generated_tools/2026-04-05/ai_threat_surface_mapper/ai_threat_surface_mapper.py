import os
import re
import yaml
from rich.console import Console
from rich.table import Table
import argparse

def scan_file(file_path):
    """
    Scans a single file for potential vulnerabilities.

    Args:
        file_path (str): Path to the file to scan.

    Returns:
        list: A list of detected vulnerabilities.
    """
    vulnerabilities = []
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

            # Check for hardcoded secrets (e.g., API keys)
            if re.search(r'(?i)(api[_-]?key|secret)["\']?\s*[:=]\s*["\']\w+["\']', content):
                vulnerabilities.append("Hardcoded API key or secret detected.")

            # Check for insecure HTTP usage
            if re.search(r'http://', content):
                vulnerabilities.append("Insecure HTTP usage detected.")

            # Check for weak encryption practices (e.g., use of MD5)
            if re.search(r'(?i)md5\(', content):
                vulnerabilities.append("Weak encryption (MD5) detected.")

    except Exception as e:
        vulnerabilities.append(f"Error reading file: {e}")

    return vulnerabilities

def scan_directory(directory_path):
    """
    Scans a directory for potential vulnerabilities by analyzing its files.

    Args:
        directory_path (str): Path to the directory to scan.

    Returns:
        dict: A dictionary of files and their associated vulnerabilities.
    """
    results = {}
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if file.endswith(('.py', '.yaml', '.yml', '.json', '.txt')):
                results[file_path] = scan_file(file_path)
    return results

def generate_report(scan_results):
    """
    Generates a security report from the scan results.

    Args:
        scan_results (dict): A dictionary of files and their vulnerabilities.

    Returns:
        str: A formatted security report.
    """
    console = Console()
    table = Table(title="AI Threat Surface Mapper - Security Report")

    table.add_column("File", style="cyan", no_wrap=True)
    table.add_column("Vulnerabilities", style="red")

    for file, vulnerabilities in scan_results.items():
        if vulnerabilities:
            table.add_row(file, "\n".join(vulnerabilities))
        else:
            table.add_row(file, "No issues detected")

    console.print(table)

def main():
    parser = argparse.ArgumentParser(description="AI Threat Surface Mapper - Scan AI model files and code for vulnerabilities.")
    parser.add_argument('--path', type=str, required=True, help="Path to the file or directory to scan.")

    args = parser.parse_args()
    path = args.path

    if not os.path.exists(path):
        print("Error: The specified path does not exist.")
        return

    if os.path.isfile(path):
        scan_results = {path: scan_file(path)}
    elif os.path.isdir(path):
        scan_results = scan_directory(path)
    else:
        print("Error: The specified path is neither a file nor a directory.")
        return

    generate_report(scan_results)

if __name__ == "__main__":
    main()