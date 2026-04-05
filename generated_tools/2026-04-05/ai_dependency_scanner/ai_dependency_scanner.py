import argparse
import os
import subprocess
import json
from rich.console import Console
from rich.table import Table

def scan_dependencies(requirements_path):
    """
    Scans the given requirements file for outdated or vulnerable dependencies.

    Args:
        requirements_path (str): Path to the requirements.txt file.

    Returns:
        list: A list of dictionaries containing dependency information and vulnerabilities.
    """
    console = Console()

    if not os.path.exists(requirements_path):
        console.print(f"[red]Error: File {requirements_path} does not exist.[/red]")
        return []

    try:
        # Run pip-audit to check for vulnerabilities
        result = subprocess.run(
            ["pip-audit", "-r", requirements_path, "--format", "json"],
            capture_output=True,
            text=True,
            check=True,
        )
        vulnerabilities = json.loads(result.stdout)
        return vulnerabilities
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "Unknown error"
        console.print(f"[red]Error running pip-audit: {error_message}[/red]")
        return []
    except json.JSONDecodeError:
        console.print("[red]Error: Failed to parse JSON output from pip-audit.[/red]")
        return []

def display_report(vulnerabilities):
    """
    Displays the vulnerability report in a tabular format.

    Args:
        vulnerabilities (list): A list of dictionaries containing vulnerability information.
    """
    console = Console()

    if not vulnerabilities:
        console.print("[green]No vulnerabilities found![/green]")
        return

    table = Table(title="AI Dependency Vulnerability Report")
    table.add_column("Package", style="cyan", no_wrap=True)
    table.add_column("Version", style="magenta")
    table.add_column("Vulnerability", style="red")
    table.add_column("Description", style="yellow")
    table.add_column("Fix Version", style="green")

    for vuln in vulnerabilities:
        package = vuln.get("name", "N/A")
        version = vuln.get("version", "N/A")
        for issue in vuln.get("vulns", []):
            vuln_id = issue.get("id", "N/A")
            description = issue.get("description", "N/A")
            fix_version = issue.get("fix_version", "N/A")
            table.add_row(package, version, vuln_id, description, fix_version)

    console.print(table)

def main():
    parser = argparse.ArgumentParser(
        description="AI Dependency Scanner: Scans Python projects for outdated or vulnerable dependencies in AI-related libraries."
    )
    parser.add_argument(
        "--requirements",
        type=str,
        required=True,
        help="Path to the requirements.txt file to scan.",
    )

    args = parser.parse_args()
    requirements_path = args.requirements

    vulnerabilities = scan_dependencies(requirements_path)
    display_report(vulnerabilities)

if __name__ == "__main__":
    main()
