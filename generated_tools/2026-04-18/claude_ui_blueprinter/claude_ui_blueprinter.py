import os
import argparse
import requests
from flask import Blueprint
from django.conf import settings
from django.urls import path
from django.http import HttpResponse

def generate_blueprint(framework, colorscheme, layout, output_dir):
    """
    Generate a Flask or Django blueprint based on the provided specifications.

    Args:
        framework (str): The framework to use ('flask' or 'django').
        colorscheme (str): The color scheme for the UI.
        layout (str): The layout for the UI.
        output_dir (str): The directory to save the blueprint.

    Raises:
        ValueError: If the framework is not supported.
    """
    # Simulate an API call to Claude Design's AI service
    try:
        response = requests.post(
            "https://api.claude-design.com/generate-ui",
            json={"framework": framework, "colorscheme": colorscheme, "layout": layout},
            timeout=10
        )
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch UI components from Claude Design API: {e}")

    ui_components = response.json()

    if framework == 'flask':
        generate_flask_blueprint(ui_components, output_dir)
    elif framework == 'django':
        generate_django_blueprint(ui_components, output_dir)
    else:
        raise ValueError("Unsupported framework. Choose either 'flask' or 'django'.")

def generate_flask_blueprint(ui_components, output_dir):
    """Generate a Flask blueprint."""
    os.makedirs(output_dir, exist_ok=True)
    blueprint_code = f"""
from flask import Blueprint, render_template

ui_blueprint = Blueprint('ui', __name__)

@ui_blueprint.route('/')
def home():
    return "{ui_components['html']}"
"""
    with open(os.path.join(output_dir, 'ui_blueprint.py'), 'w') as f:
        f.write(blueprint_code)

def generate_django_blueprint(ui_components, output_dir):
    """Generate a Django blueprint."""
    os.makedirs(output_dir, exist_ok=True)
    views_code = f"""
from django.http import HttpResponse

def home(request):
    return HttpResponse("{ui_components['html']}")
"""
    urls_code = f"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
"""
    with open(os.path.join(output_dir, 'views.py'), 'w') as f:
        f.write(views_code)
    with open(os.path.join(output_dir, 'urls.py'), 'w') as f:
        f.write(urls_code)

def main():
    parser = argparse.ArgumentParser(description="Generate Flask or Django blueprints for UIs using Claude Design API.")
    parser.add_argument('--framework', required=True, choices=['flask', 'django'], help="The framework to generate the blueprint for.")
    parser.add_argument('--colorscheme', required=True, help="The color scheme for the UI.")
    parser.add_argument('--layout', required=True, help="The layout for the UI.")
    parser.add_argument('--output-dir', required=True, help="The directory to save the generated blueprint.")

    args = parser.parse_args()

    try:
        generate_blueprint(args.framework, args.colorscheme, args.layout, args.output_dir)
        print(f"Blueprint generated successfully in {args.output_dir}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()