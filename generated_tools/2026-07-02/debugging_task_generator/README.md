# Debugging Task Generator

## Overview
This script generates reproducible debugging scenarios by introducing controlled bugs into user-provided codebases. It enables AI developers to assess agents on their debugging capabilities in a standardized way.

## Installation

Install the required dependency:

```bash
pip install black
```

## Usage

Run the script with the following arguments:

```bash
python debugging_task_generator.py --code_dir <path_to_code_directory> --config <path_to_config_file>
```

### Arguments

- `--code_dir`: Path to the directory containing Python source code files.
- `--config`: Path to the JSON configuration file specifying bug types and locations.

## Configuration File Format

The configuration file should be a JSON file with the following structure:

```json
{
  "files": [
    {
      "file": "example.py",
      "bug_type": "syntax"
    },
    {
      "file": "another_example.py",
      "bug_type": "logic"
    }
  ]
}
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_debugging_task_generator.py
```

## License

This project is licensed under the MIT License.