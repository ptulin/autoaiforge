# Claude UI Customizer

## Description
Claude UI Customizer is a Python library that integrates with Claude Design APIs to fetch, modify, and customize existing UI designs programmatically. It allows developers to input existing layouts and apply modifications such as theme changes, resizing, or component replacements.

## Installation

Install the required dependencies using pip:

```bash
pip install requests==2.31.0 pydantic==1.10.7
```

## Usage

### Example

```python
from claude_ui_customizer import customize_ui

api_url = "http://mockapi.com"
design_id = "12345"

# Fetch and modify a design
existing_design = fetch_design(api_url, design_id)
new_design = modify_design(existing_design, theme='dark', resize=(1920, 1080))

# Update the design in the API
update_design(api_url, new_design)
```

Alternatively, use the CLI:

```bash
python claude_ui_customizer.py http://mockapi.com 12345 --theme dark --resize 1920 1080 --output modified_design.json
```

## Features
- Fetches existing UI designs from Claude Design API.
- Modifies designs with new themes, resizing, or component replacements.
- Outputs modified designs as JSON files or updates them directly in the API.
- Easy integration with existing Python projects.

## License
MIT License