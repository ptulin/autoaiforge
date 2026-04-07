# Source Code Provenance Checker

## Description
This tool analyzes AI source code to detect potential intellectual property violations by comparing code snippets against publicly available repositories. It helps developers ensure compliance and safeguard proprietary code.

## Installation
Install the required dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage
Run the tool using the following command:

```bash
python source_code_provenance_checker.py --path <path_to_source_code_file>
```

Replace `<path_to_source_code_file>` with the path to the source code file you want to analyze.

## Testing
Run the tests using pytest:

```bash
pytest test_source_code_provenance_checker.py
```

## Requirements
- Python 3.7+
- requests
- pytest

## License
MIT License
