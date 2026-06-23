# Repository Commit Analyzer

## Overview
The Repository Commit Analyzer is a Python tool that analyzes the commit history of a local Git repository to generate insights into trends, contributor activity, and code evolution. It provides visualizations such as commit frequency over time and contributor activity.

## Features
- Analyze commit frequency over time.
- Analyze contributor activity.
- Generate visualizations for commit frequency and contributor activity.

## Requirements
- Python 3.7+
- Required Python packages:
  - `matplotlib`
  - `numpy`
  - `GitPython`

## Installation
Install the required Python packages using pip:

```bash
pip install matplotlib numpy gitpython
```

## Usage
Run the tool from the command line:

```bash
python repo_commit_analyzer.py --repo <path_to_local_git_repo> --output <output_json_file> --visualizations <output_visualizations_dir>
```

- `--repo`: Path to the local Git repository to analyze.
- `--output`: Path to save the analysis results as a JSON file.
- `--visualizations`: Directory to save the visualizations (default: `visualizations`).

### Example
```bash
python repo_commit_analyzer.py --repo ./my-repo --output analysis.json --visualizations ./output_visualizations
```

## Testing
To run the tests, install `pytest` and run the test suite:

```bash
pip install pytest
pytest test_repo_commit_analyzer.py
```

The tests include:
- Verifying the analysis of a repository with mock commits.
- Ensuring visualizations are generated correctly.
- Handling of invalid repository paths.
- Handling of bare repositories.
- Handling of empty repositories.

## License
This project is licensed under the MIT License.