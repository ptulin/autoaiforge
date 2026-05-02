# Auto Patch Applier

## Overview
Auto Patch Applier integrates with AI models to identify, download, and apply patches to your codebase without manual intervention. It uses a sandboxing approach to test patches before applying them to ensure stability.

## Installation

Install the required Python package:

```bash
pip install openai
```

## Usage

Run the tool using the following command:

```bash
python auto_patch_applier.py --path <project_path> [--test_sandbox] [--rollback]
```

### Arguments

- `--path`: Path to the project directory (required).
- `--test_sandbox`: Enable sandbox testing before applying the patch (optional).
- `--rollback`: Rollback the last applied patch (optional).

### Example

```bash
python auto_patch_applier.py --path ./my_project --test_sandbox
```

This command will fetch patch suggestions for the codebase in `./my_project`, test the patch in a sandbox environment, and apply the patch if the tests pass.

To rollback the last applied patch:

```bash
python auto_patch_applier.py --path ./my_project --rollback
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests:

```bash
pytest test_auto_patch_applier.py
```

All tests should pass without requiring network access.