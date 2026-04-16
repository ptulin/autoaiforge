# Code Optimizer Agent

## Overview
The Code Optimizer Agent is a Python tool that analyzes Python scripts for performance and readability improvements. It provides optimized versions of input code alongside explanations for the changes, focusing on enhancing code efficiency, reducing complexity, and following best practices.

## Features
- Formats code using the Black code formatter.
- Provides AI-generated suggestions for improving code performance and readability using OpenAI's GPT-4.
- Saves the optimized code and a detailed change log to separate files.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the command line:

```bash
python code_optimizer_agent.py --file <path_to_python_script> --api-key <your_openai_api_key>
```

- `--file`: Path to the Python script file to optimize.
- `--api-key`: Your OpenAI API key for generating suggestions.

## Example

```bash
python code_optimizer_agent.py --file example.py --api-key sk-xxxxxxxxxx
```

After running the command, the tool will generate two files:
1. `optimized_<original_filename>`: Contains the optimized Python code.
2. `change_log_<original_filename>.txt`: Contains the change log with explanations for the optimizations.

## Testing

Run the tests using `pytest`:

```bash
pytest test_code_optimizer_agent.py
```

## Requirements
- Python 3.7+
- `openai`
- `black`
- `pytest`

## License
This project is licensed under the MIT License.