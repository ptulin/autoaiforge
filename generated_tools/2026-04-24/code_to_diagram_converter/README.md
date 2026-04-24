# Code-to-Diagram Converter

## Description
This CLI tool uses OpenAI's GPT-5.5 to transform code logic into visual flowcharts or UML diagrams. It is particularly helpful in analyzing complex functions or systems and generating visual documentation.

## Features
- Converts code logic into flowcharts or UML diagrams.
- Supports multiple output formats: PNG, SVG, and DOT.
- Uses OpenAI's GPT-5.5 for generating flowchart descriptions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool using the command line:

```bash
python code_to_diagram_converter.py --code <path_to_code_file_or_code_snippet> --output <output_file> --api-key <your_openai_api_key>
```

### Arguments
- `--code`: Path to the code file or a code snippet as a string.
- `--output`: Output diagram file (e.g., `diagram.png`, `diagram.svg`, `diagram.dot`).
- `--api-key`: Your OpenAI API key.

### Example

```bash
python code_to_diagram_converter.py --code "def add(a, b):\n    return a + b" --output diagram.png --api-key your_openai_api_key
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_code_to_diagram_converter.py
```

## Requirements

- Python 3.7+
- openai
- graphviz
- pytest

## Notes

- Ensure that Graphviz is installed and its executables are available in your system's PATH. You can download Graphviz from [https://graphviz.org/download/](https://graphviz.org/download/).
- The tool requires an OpenAI API key to function. You can obtain one from [OpenAI](https://platform.openai.com/).
