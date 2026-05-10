# Dream Diff Visualizer

## Overview

The Dream Diff Visualizer is a Python CLI tool designed to compare two dreaming session outputs from Claude AI. It generates an interactive visual diff in HTML format, helping developers pinpoint specific areas of improvement or regression in the model's updates.

## Features

- Compare two text files or JSON files.
- Automatically formats JSON files for better readability.
- Generates an interactive HTML diff that highlights changes.

## Installation

1. Clone this repository.
2. Install the required dependencies using pip:

```bash
pip install jinja2
```

## Usage

Run the tool from the command line with the following arguments:

```bash
python dream_diff_visualizer.py --file1 <path_to_first_file> --file2 <path_to_second_file> --output <path_to_output_html>
```

### Example

```bash
python dream_diff_visualizer.py --file1 session1.json --file2 session2.json --output diff.html
```

This will generate an HTML file named `diff.html` containing the visual diff between `session1.json` and `session2.json`.

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run:

```bash
pytest test_dream_diff_visualizer.py
```

All tests should pass successfully.

## License

This project is licensed under the MIT License.