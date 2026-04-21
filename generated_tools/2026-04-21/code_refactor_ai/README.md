# Code Refactor AI

Code Refactor AI is a CLI tool that leverages AI models to analyze and refactor Python codebases. It identifies repetitive patterns, unused imports, inefficient loops, and suggests improvements or directly applies optimizations to enhance readability and performance.

## Features
- AI-powered code refactoring for Python projects
- Optimizes loops, imports, and code structure
- Provides a detailed report or applies changes directly

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Analyze and Suggest Improvements

```bash
python code_refactor_ai.py --input my_project
```

### Apply Changes Directly

```bash
python code_refactor_ai.py --input my_project --apply
```

## Example

Analyze a single file:

```bash
python code_refactor_ai.py --input script.py
```

Analyze and apply changes to a directory:

```bash
python code_refactor_ai.py --input my_project --apply
```

## License

This project is licensed under the MIT License.