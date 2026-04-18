# Claude Theme Builder

Claude Theme Builder is a Python tool that generates custom CSS themes and component styles by connecting with the Claude Design API. Developers can specify branding details (e.g., primary colors, fonts, spacing) through a JSON configuration file, and the tool produces a complete CSS file tailored to their requirements.

## Features
- Generates responsive, modern CSS themes using Claude Design.
- Supports multiple framework-specific output formats (e.g., Material-UI, Bootstrap).
- Merges user-provided branding details with default design settings from Claude Design.
- Outputs a complete CSS file ready for use in your projects.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-repo/claude_theme_builder.git
    cd claude_theme_builder
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

To generate a CSS theme, run the following command:

```bash
python claude_theme_builder.py --config <path_to_config.json> --framework <framework_name> --output <output_file.css>
```

### Example

```bash
python claude_theme_builder.py --config branding.json --framework bootstrap --output theme.css
```

- `--config`: Path to a JSON file specifying branding details (e.g., primary colors, fonts, spacing).
- `--framework`: The framework for which the CSS should be generated. Supported options: `bootstrap`, `material-ui`.
- `--output`: Path to save the generated CSS file.

## Development

### Running Tests

To run the tests, use `pytest`:

```bash
pytest test_claude_theme_builder.py
```

### Mocking External Calls

The tests mock all external network calls to ensure they pass without network access.

## License

This project is licensed under the MIT License. See the LICENSE file for details.