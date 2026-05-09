import os
import json
from pathlib import Path
from typing import Optional
import requests
import typer
from jinja2 import Template

app = typer.Typer()

TEMPLATES = {
    "nlp": "# NLP Workflow Integration\n\nfrom gemini import GeminiModel\n\nmodel = GeminiModel(version='{{ model_version }}')\n\ndef process_text(text):\n    result = model.analyze_text(text)\n    return result\n",
    "cv": "# Computer Vision Workflow Integration\n\nfrom gemini import GeminiModel\n\nmodel = GeminiModel(version='{{ model_version }}')\n\ndef process_image(image_path):\n    with open(image_path, 'rb') as img_file:\n        result = model.analyze_image(img_file)\n    return result\n"
}

CONFIG_TEMPLATE = """{
    "model_version": "{{ model_version }}",
    "workflow_type": "{{ workflow_type }}"
}
"""

API_URL = "https://api.gemini.com/models/validate"

def validate_model_version(model_version: str) -> bool:
    """Validate the Gemini model version via API."""
    try:
        response = requests.get(f"{API_URL}?version={model_version}")
        response.raise_for_status()
        data = response.json()
        return data.get("valid", False)
    except requests.RequestException as e:
        typer.echo(f"Error validating model version: {e}", err=True)
        return False

def generate_files(workflow_type: str, model_version: str, output_dir: Path):
    """Generate integration files based on the workflow type and model version."""
    if workflow_type not in TEMPLATES:
        typer.echo(f"Unsupported workflow type: {workflow_type}", err=True)
        raise typer.Exit(code=1)

    if not validate_model_version(model_version):
        typer.echo(f"Invalid or unsupported model version: {model_version}", err=True)
        raise typer.Exit(code=1)

    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate code file
    template = Template(TEMPLATES[workflow_type])
    code_content = template.render(model_version=model_version)
    code_file = output_dir / "integration.py"
    code_file.write_text(code_content)

    # Generate config file
    config_template = Template(CONFIG_TEMPLATE)
    config_content = config_template.render(model_version=model_version, workflow_type=workflow_type)
    config_file = output_dir / "config.json"
    config_file.write_text(config_content)

    typer.echo(f"Files generated successfully in {output_dir}")

@app.command()
def main(
    model: str = typer.Option(..., help="Gemini model version to integrate, e.g., gemini-3"),
    workflow: str = typer.Option(..., help="Workflow type, e.g., nlp or cv"),
    output: Path = typer.Option(..., help="Output directory for generated files")
):
    """Gemini Workflow Integration Tool"""
    try:
        generate_files(workflow, model, output)
    except Exception as e:
        typer.echo(f"An error occurred: {e}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
