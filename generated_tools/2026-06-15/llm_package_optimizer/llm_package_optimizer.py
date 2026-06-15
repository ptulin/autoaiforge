import os
import argparse
import subprocess
import yaml
from rich.console import Console
from rich.table import Table

def parse_requirements(file_path):
    """Parse a requirements.txt file into a list of dependencies."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as f:
        lines = f.readlines()

    dependencies = [line.strip() for line in lines if line.strip() and not line.startswith('#')]
    return dependencies

def check_hardware_compatibility():
    """Check for GPU compatibility and return relevant libraries."""
    try:
        result = subprocess.run(['nvidia-smi'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            return ['torch', 'tensorflow-gpu']
        else:
            return ['torch-cpu', 'tensorflow']
    except FileNotFoundError:
        return ['torch-cpu', 'tensorflow']

def optimize_dependencies(dependencies):
    """Optimize dependencies by removing unused or redundant packages."""
    optimized = []
    for dep in dependencies:
        if 'torch' in dep or 'tensorflow' in dep:
            continue  # Skip LLM-related packages for now
        optimized.append(dep)

    # Add hardware-compatible LLM packages
    optimized.extend(check_hardware_compatibility())
    return optimized

def write_requirements(dependencies, output_path):
    """Write the optimized dependencies to a new requirements file."""
    with open(output_path, 'w') as f:
        for dep in dependencies:
            f.write(f"{dep}\n")

def main():
    parser = argparse.ArgumentParser(description="LLM Package Optimizer")
    parser.add_argument('--input', required=True, help="Path to the input requirements.txt file")
    parser.add_argument('--output', required=True, help="Path to save the optimized requirements.txt file")
    args = parser.parse_args()

    console = Console()

    try:
        console.print("[bold green]Parsing requirements file...[/bold green]")
        dependencies = parse_requirements(args.input)

        console.print("[bold green]Optimizing dependencies...[/bold green]")
        optimized_dependencies = optimize_dependencies(dependencies)

        console.print("[bold green]Writing optimized requirements...[/bold green]")
        write_requirements(optimized_dependencies, args.output)

        console.print("[bold green]Optimization complete![/bold green]")

        table = Table(title="Optimized Dependencies")
        table.add_column("Dependency")
        for dep in optimized_dependencies:
            table.add_row(dep)

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

if __name__ == "__main__":
    main()