# Claude UI Blueprint Generator

## Overview
The `claude_ui_blueprint_generator` is a CLI tool that uses Claude Design's APIs to generate UI blueprints in JSON or Figma-compatible formats from simple textual descriptions of user interfaces. Developers can use it to quickly prototype UI layouts or explore design ideas without manually creating wireframes.

## Features
- Generate UI blueprints in JSON or Figma-compatible formats.
- Customize the theme (e.g., dark, light) and layout style (e.g., grid, flex).
- Save the generated blueprint to a file.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_ui_blueprint_generator
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the CLI tool with the following options:

```bash
python claude_ui_blueprint_generator.py --description "dashboard with sidebar and three cards" \
    --output-format json \
    --theme dark \
    --layout-style grid \
    --output-file output.json
```

### Options
- `--description`: Textual description of the desired UI layout (required).
- `--output-format`: Output format: `json` or `figma` (required).
- `--theme`: Theme for the UI (e.g., `dark`, `light`) (optional).
- `--layout-style`: Layout style (e.g., `grid`, `flex`) (optional).
- `--output-file`: File to save the generated blueprint (default: `output.json`).

## Testing

To run the tests, use `pytest`:

```bash
pytest test_claude_ui_blueprint_generator.py
```

The tests use mocking to simulate API responses, so no network connection is required.

## Dependencies
- `requests`: For making HTTP requests to the Claude Design API.
- `click`: For building the command-line interface.
- `pytest`: For running the test suite.

## License
This project is licensed under the MIT License.