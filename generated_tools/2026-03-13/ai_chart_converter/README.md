# AI Chart Converter

## Overview

AI Chart Converter is a CLI tool that transforms AI-generated chart specifications (e.g., JSON output from AI models) into shareable HTML files or images. This tool allows developers to quickly generate static or interactive data visualizations for presentations or reports without needing to manually interpret the chart structure.

## Features

- **Interactive Charts**: Generate interactive charts using Plotly and save them as HTML files.
- **Static Charts**: Generate static charts using Matplotlib and save them as image files.

## Installation

Install the required dependencies using pip:

```bash
pip install click plotly matplotlib
```

## Usage

Run the tool from the command line:

```bash
python ai_chart_converter.py --input <input_json_path> --output <output_file_path> --style <interactive|static>
```

### Options

- `--input`: Path to the input JSON file containing the chart specification.
- `--output`: Path to the output file (HTML for interactive charts, image file for static charts).
- `--style`: Chart style. Use `interactive` for Plotly charts or `static` for Matplotlib charts.

### Example

Generate an interactive chart:

```bash
python ai_chart_converter.py --input chart.json --output chart.html --style interactive
```

Generate a static chart:

```bash
python ai_chart_converter.py --input chart.json --output chart.png --style static
```

## Testing

Run the tests using pytest:

```bash
pytest test_ai_chart_converter.py
```

## License

This project is licensed under the MIT License.