# Claude UI Blueprinter

## Description
The Claude UI Blueprinter is a command-line tool that generates Flask or Django blueprint modules for user interfaces. By leveraging the Claude Design API, this tool creates ready-to-use UI components based on high-level design specifications such as color schemes and layouts. It helps developers quickly scaffold complete UIs for their projects.

## Features
- Generates Flask or Django blueprints for UIs
- Integrates with Claude Design API for AI-driven design assets
- Supports customizable templates and branding options

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the following command:

```bash
python claude_ui_blueprinter.py --framework <framework> --colorscheme <colorscheme> --layout <layout> --output-dir <output-directory>
```

### Example

To generate a Flask blueprint with a dark color scheme and grid layout:

```bash
python claude_ui_blueprinter.py --framework flask --colorscheme dark --layout grid --output-dir ./flask_blueprint
```

To generate a Django blueprint with a light color scheme and list layout:

```bash
python claude_ui_blueprinter.py --framework django --colorscheme light --layout list --output-dir ./django_blueprint
```

## Testing

Run the tests using pytest:

```bash
pytest test_claude_ui_blueprinter.py
```

## Notes
- Ensure you have an active internet connection to access the Claude Design API.
- The tool handles API errors and invalid inputs gracefully.

## License
This project is licensed under the MIT License.
