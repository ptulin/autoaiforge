# LLM Package Optimizer

## Description
LLM Package Optimizer is a command-line tool designed to analyze and optimize Python packages and dependencies for local Large Language Model (LLM) deployments. By ensuring only the necessary libraries are installed and checking for hardware compatibility, this tool helps reduce bloat and improve performance.

## Features
- Analyze dependencies in a `requirements.txt` file or Python environment.
- Automatically remove unused or redundant packages.
- Check hardware compatibility for GPU acceleration and recommend appropriate libraries.
- Generate an optimized `requirements.txt` file.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/llm_package_optimizer.git
   cd llm_package_optimizer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To use the LLM Package Optimizer, run the following command:

```bash
python llm_package_optimizer.py --input requirements.txt --output optimized_requirements.txt
```

- `--input`: Path to the input `requirements.txt` file.
- `--output`: Path to save the optimized `requirements.txt` file.

### Example

Input `requirements.txt`:
```
torch
tensorflow
scipy
numpy
# Commented line
```

Command:
```bash
python llm_package_optimizer.py --input requirements.txt --output optimized_requirements.txt
```

Output `optimized_requirements.txt`:
```
scipy
numpy
torch
tensorflow-gpu
```

## Testing

Run the tests using `pytest`:

```bash
pytest test_llm_package_optimizer.py
```

## License

This project is licensed under the MIT License.