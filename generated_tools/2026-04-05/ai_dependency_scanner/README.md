# AI Dependency Scanner

AI Dependency Scanner is a command-line tool that scans Python projects for outdated or vulnerable dependencies in AI-related libraries (e.g., TensorFlow, PyTorch). It cross-references with public vulnerability databases to alert developers to potential risks in their AI software stack.

## Features

- Scans a `requirements.txt` file for dependencies.
- Identifies outdated or vulnerable dependencies.
- Displays a detailed vulnerability report in a tabular format.

## Installation

To use this tool, you need to have Python installed on your system. Additionally, install the required dependencies:

```bash
pip install rich
pip install pip-audit
```

## Usage

Run the tool with the following command:

```bash
python ai_dependency_scanner.py --requirements /path/to/requirements.txt
```

Replace `/path/to/requirements.txt` with the path to your `requirements.txt` file.

## Example

```bash
python ai_dependency_scanner.py --requirements requirements.txt
```

This will scan the dependencies listed in `requirements.txt` and display a report of any vulnerabilities found.

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then run:

```bash
pytest test_ai_dependency_scanner.py
```

All tests should pass successfully.

## License

This project is licensed under the MIT License.