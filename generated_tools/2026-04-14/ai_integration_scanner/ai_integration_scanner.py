import os
import re
import ast
import argparse
from colorama import Fore, Style

def scan_file(file_path):
    """
    Scans a single Python file for security vulnerabilities.

    Args:
        file_path (str): Path to the Python file to scan.

    Returns:
        list: A list of dictionaries containing details of security issues found.
    """
    issues = []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Check for hardcoded API keys
        api_key_pattern = re.compile(r'["\'](sk-[a-zA-Z0-9]{32,})["\']')
        for line_no, line in enumerate(content.splitlines(), start=1):
            if api_key_pattern.search(line):
                issues.append({
                    'line': line_no,
                    'issue': 'Hardcoded API key detected.',
                    'recommendation': 'Remove hardcoded API keys and use environment variables instead.'
                })

        # Check for unencrypted HTTP requests
        http_pattern = re.compile(r'http://')
        for line_no, line in enumerate(content.splitlines(), start=1):
            if http_pattern.search(line):
                issues.append({
                    'line': line_no,
                    'issue': 'Unencrypted HTTP request detected.',
                    'recommendation': 'Use HTTPS instead of HTTP for secure communication.'
                })

        # Check for unsafe eval or exec usage
        unsafe_patterns = [r'eval\(', r'exec\(']
        for pattern in unsafe_patterns:
            unsafe_pattern = re.compile(pattern)
            for line_no, line in enumerate(content.splitlines(), start=1):
                if unsafe_pattern.search(line):
                    issues.append({
                        'line': line_no,
                        'issue': f'Usage of unsafe function {pattern[:-2]} detected.',
                        'recommendation': 'Avoid using eval or exec and use safer alternatives.'
                    })

    except (OSError, UnicodeDecodeError) as e:
        print(Fore.RED + f"Error reading file {file_path}: {e}" + Style.RESET_ALL)

    return issues

def scan_directory(directory_path):
    """
    Scans all Python files in a directory for security vulnerabilities.

    Args:
        directory_path (str): Path to the directory to scan.

    Returns:
        list: A list of issues found across all files.
    """
    all_issues = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                issues = scan_file(file_path)
                for issue in issues:
                    issue['file'] = file_path
                all_issues.extend(issues)

    return all_issues

def main():
    parser = argparse.ArgumentParser(
        description="AI Integration Security Scanner: Scans Python code for security vulnerabilities in AI integrations."
    )
    parser.add_argument('--path', required=True, help="Path to a directory or file containing Python code.")
    args = parser.parse_args()

    path = args.path

    if os.path.isfile(path):
        issues = scan_file(path)
        for issue in issues:
            print(Fore.YELLOW + f"File: {path}, Line: {issue['line']}" + Style.RESET_ALL)
            print(Fore.RED + f"Issue: {issue['issue']}" + Style.RESET_ALL)
            print(Fore.GREEN + f"Recommendation: {issue['recommendation']}" + Style.RESET_ALL)
            print()
    elif os.path.isdir(path):
        issues = scan_directory(path)
        for issue in issues:
            print(Fore.YELLOW + f"File: {issue['file']}, Line: {issue['line']}" + Style.RESET_ALL)
            print(Fore.RED + f"Issue: {issue['issue']}" + Style.RESET_ALL)
            print(Fore.GREEN + f"Recommendation: {issue['recommendation']}" + Style.RESET_ALL)
            print()
    else:
        print(Fore.RED + "Invalid path provided. Please specify a valid file or directory." + Style.RESET_ALL)

if __name__ == "__main__":
    main()