import argparse
import json
import csv
from tabulate import tabulate
from bs4 import BeautifulSoup
import requests

FRAMEWORK_METADATA = {
    "tensorflow": {
        "url": "https://www.tensorflow.org/",
        "features": ["Model Serialization", "GPU Support", "TPU Support", "Built-in Optimizers"]
    },
    "pytorch": {
        "url": "https://pytorch.org/",
        "features": ["Model Serialization", "GPU Support", "Distributed Training", "Dynamic Computation Graphs"]
    },
    "jax": {
        "url": "https://jax.readthedocs.io/",
        "features": ["GPU Support", "TPU Support", "Automatic Differentiation"]
    }
}

def fetch_framework_data(framework):
    if framework not in FRAMEWORK_METADATA:
        raise ValueError(f"Framework '{framework}' is not supported.")

    metadata = FRAMEWORK_METADATA[framework]
    url = metadata["url"]

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else "No Title Found"
        return {
            "name": framework,
            "url": url,
            "title": title,
            "features": metadata["features"]
        }
    except requests.RequestException as e:
        return {
            "name": framework,
            "url": url,
            "title": "Error fetching data",
            "features": metadata["features"],
            "error": str(e)
        }

def generate_feature_matrix(frameworks):
    data = []
    for framework in frameworks:
        framework_data = fetch_framework_data(framework)
        data.append({
            "Framework": framework_data["name"],
            "Title": framework_data["title"],
            "URL": framework_data["url"],
            "Features": ", ".join(framework_data["features"]),
            "Error": framework_data.get("error", "")
        })
    return data

def save_output(data, output_format, output_file):
    if output_format == "json":
        with open(output_file, "w") as f:
            json.dump(data, f, indent=4)
    elif output_format == "csv":
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    elif output_format == "markdown":
        table = tabulate(data, headers="keys", tablefmt="github")
        with open(output_file, "w") as f:
            f.write(table)
    else:
        raise ValueError("Unsupported output format. Choose from 'json', 'csv', or 'markdown'.")

def main():
    parser = argparse.ArgumentParser(description="AI Framework Feature Matrix Generator")
    parser.add_argument("--frameworks", nargs="+", required=True, help="List of frameworks to compare")
    parser.add_argument("--output", required=True, choices=["json", "csv", "markdown"], help="Output format")
    parser.add_argument("--output-file", required=True, help="Output file path")

    args = parser.parse_args()

    try:
        data = generate_feature_matrix(args.frameworks)
        save_output(data, args.output, args.output_file)
        print(f"Feature matrix saved to {args.output_file} in {args.output} format.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()