import json
import requests
import click

def generate_ui_blueprint(description, output_format, theme=None, layout_style=None):
    """
    Generates a UI blueprint based on the provided description and options.

    Args:
        description (str): Textual description of the desired UI layout.
        output_format (str): The desired output format ('json' or 'figma').
        theme (str, optional): Theme for the UI (e.g., 'dark', 'light').
        layout_style (str, optional): Layout style (e.g., 'grid', 'flex').

    Returns:
        dict: The generated UI blueprint.

    Raises:
        ValueError: If the output format is invalid.
        RuntimeError: For network-related issues or API errors.
    """
    if output_format not in ["json", "figma"]:
        raise ValueError("Invalid output format. Choose 'json' or 'figma'.")

    api_url = "https://api.claudedesign.com/generate_blueprint"
    payload = {
        "description": description,
        "output_format": output_format,
        "theme": theme,
        "layout_style": layout_style
    }

    try:
        response = requests.post(api_url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        raise RuntimeError(f"Error communicating with Claude Design API: {e}")

@click.command()
@click.option('--description', required=True, help='Textual description of the desired UI layout.')
@click.option('--output-format', required=True, type=click.Choice(['json', 'figma']), help='Output format: json or figma.')
@click.option('--theme', default=None, help='Theme for the UI (e.g., dark, light).')
@click.option('--layout-style', default=None, help='Layout style (e.g., grid, flex).')
@click.option('--output-file', default='output.json', help='File to save the generated blueprint.')
def main(description, output_format, theme, layout_style, output_file):
    """
    CLI entry point for generating UI blueprints.
    """
    try:
        blueprint = generate_ui_blueprint(description, output_format, theme, layout_style)
        with open(output_file, 'w') as f:
            json.dump(blueprint, f, indent=4)
        click.echo(f"UI blueprint successfully saved to {output_file}.")
    except ValueError as ve:
        click.echo(f"Error: {ve}")
    except RuntimeError as re:
        click.echo(f"Error: {re}")
    except Exception as e:
        click.echo(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()