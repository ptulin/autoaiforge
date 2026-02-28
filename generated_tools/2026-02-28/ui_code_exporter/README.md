# UI Code Exporter

## Description
UI Code Exporter is a Python tool that leverages OpenAI Codex to generate production-ready front-end code (HTML/CSS/JS) directly from exported UI/UX design files (e.g., JSON or SVG from Figma). It simplifies the process of turning designs into functional code with AI-driven suggestions for best practices.

## Features
- Supports JSON and SVG design files.
- Generates code for React, Vue, or plain HTML/CSS/JS.
- Saves the generated code to a specified output directory.

## Requirements
- Python 3.7+
- `openai` Python package
- `svgwrite` Python package

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/ui-code-exporter.git
   cd ui-code-exporter
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
```bash
python ui_code_exporter.py --input <design_file> --framework <framework> --output <output_directory>
```

### Arguments
- `--input`: Path to the input design file (JSON or SVG).
- `--framework`: Framework for the generated code. Options: `react`, `vue`, `html`. Default: `html`.
- `--output`: Path to the output directory.

### Example
```bash
python ui_code_exporter.py --input design.json --framework react --output ./output
```

## Testing
To run the tests, install `pytest` and run:
```bash
pytest test_ui_code_exporter.py
```

## License
MIT License