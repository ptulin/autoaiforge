import os
import click
from packaging.requirements import Requirement
from packaging.version import Version
from safety import safety
from safety.formatter import BareFormatter
from safety.safety import check
from safety.util import read_vulnerabilities

def parse_dependencies(file_path):
    """Parse dependencies from a requirements.txt or Pipfile."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    dependencies = []
    for line in lines:
        try:
            dependencies.append(Requirement(line.strip()))
        except:
            pass
    return dependencies

def check_dependencies(dependencies):
    """Check dependencies against known CVEs."""
    vulnerabilities = []
    for dep in dependencies:
        vulnerabilities.append(check(dep))
    return vulnerabilities

@click.command()
@click.option('--file', required=True, help='Path to requirements.txt or Pipfile')
def main(file):
    """Main entry point."""
    deps = parse_dependencies(file)
    vulns = check_dependencies(deps)
    print(vulns)

if __name__ == '__main__':
    main()