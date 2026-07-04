import os
import ast
from rich.console import Console
from rich.table import Table

console = Console()

def analyze_file(file_path):
    """
    Analyze a single Python file for deprecated or insecure usages of AI/ML libraries.

    Args:
        file_path (str): Path to the Python file.

    Returns:
        dict: Analysis results containing deprecated methods and insecure configurations.
    """
    results = {
        "deprecated_methods": [],
        "insecure_configurations": []
    }

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename=file_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    # Check for deprecated methods
                    if node.func.attr in ["fit_transform", "predict_proba"]:
                        results["deprecated_methods"].append(node.func.attr)

                    # Check for insecure configurations
                    if node.func.attr == "train":
                        for keyword in node.keywords:
                            if keyword.arg == "shuffle" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
                                results["insecure_configurations"].append("shuffle=True in training")

    except Exception as e:
        console.print(f"[red]Error analyzing {file_path}: {e}")

    return results

def analyze_directory(directory_path):
    """
    Analyze all Python files in a directory.

    Args:
        directory_path (str): Path to the directory.

    Returns:
        list: List of analysis results for each file.
    """
    if not os.path.isdir(directory_path):
        raise ValueError(f"Invalid directory path: {directory_path}")

    analysis_results = []

    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                results = analyze_file(file_path)
                analysis_results.append({"file": file_path, "results": results})

    return analysis_results

def generate_report(analysis_results):
    """
    Generate a detailed report from analysis results.

    Args:
        analysis_results (list): List of analysis results.
    """
    table = Table(title="ML Dependency Inspector Report")

    table.add_column("File", style="cyan")
    table.add_column("Deprecated Methods", style="magenta")
    table.add_column("Insecure Configurations", style="red")

    for result in analysis_results:
        deprecated_methods = ", ".join(result["results"]["deprecated_methods"])
        insecure_configurations = ", ".join(result["results"]["insecure_configurations"])
        table.add_row(result["file"], deprecated_methods or "None", insecure_configurations or "None")

    console.print(table)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="ML Dependency Inspector")
    parser.add_argument("--path", required=True, help="Path to the directory containing Python files to analyze.")
    args = parser.parse_args()

    try:
        analysis_results = analyze_directory(args.path)
        generate_report(analysis_results)
    except ValueError as e:
        console.print(f"[red]{e}")
    except Exception as e:
        console.print(f"[red]An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
