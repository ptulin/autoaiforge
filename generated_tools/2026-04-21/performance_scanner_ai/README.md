# Performance Scanner AI

Performance Scanner AI is a Python tool that scans Python codebases and identifies performance bottlenecks using AI analysis. It highlights sections of code that are computationally expensive and suggests alternative implementations.

## Features
- Analyze Python code for performance bottlenecks.
- Suggest optimizations for computationally expensive code.

## Installation

Install the required dependencies:

```bash
pip install openai pygments
```

## Usage

Run the tool from the command line:

```bash
python performance_scanner_ai.py <path_to_python_file>
```

Example:

```bash
python performance_scanner_ai.py example.py
```

## Testing

Run the tests using pytest:

```bash
pytest test_performance_scanner_ai.py
```

## License

MIT License