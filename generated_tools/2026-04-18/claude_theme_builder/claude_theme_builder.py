import argparse
import json
import os
import requests
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')

class ThemeBuilder:
    def __init__(self, config, framework):
        self.config = config
        self.framework = framework
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

    def generate_css(self):
        try:
            template = self.env.get_template(f'{self.framework}.css.j2')
        except Exception as e:
            raise ValueError(f"Template for framework '{self.framework}' not found.") from e

        css = template.render(self.config)
        return css

def fetch_design_defaults():
    url = "https://api.claude.design/defaults"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError("Failed to fetch design defaults from Claude Design API.") from e

def load_config(config_path):
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"The configuration file '{config_path}' does not exist.")
    except json.JSONDecodeError:
        raise ValueError(f"The configuration file '{config_path}' is not a valid JSON file.")

def main():
    parser = argparse.ArgumentParser(description="Claude Theme Builder: Generate custom CSS themes.")
    parser.add_argument('--config', required=True, help="Path to the JSON configuration file.")
    parser.add_argument('--framework', required=True, choices=['bootstrap', 'material-ui'], help="Framework for the CSS output.")
    parser.add_argument('--output', required=True, help="Output path for the generated CSS file.")
    args = parser.parse_args()

    try:
        config = load_config(args.config)
        defaults = fetch_design_defaults()
        config = {**defaults, **config}  # Merge defaults with user config

        builder = ThemeBuilder(config, args.framework)
        css = builder.generate_css()

        with open(args.output, 'w') as output_file:
            output_file.write(css)

        print(f"CSS theme successfully generated and saved to '{args.output}'.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()