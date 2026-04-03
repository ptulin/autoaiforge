# Code Review Assistant

## Description
Code Review Assistant is a lightweight CLI tool that integrates with OpenAI's Claude AI to perform automated code reviews. Developers can use this tool to analyze Python code for potential bugs, performance issues, and adherence to best practices. It provides a detailed review report, either printed to the console or saved in YAML format, making it a great on-demand alternative to manual code reviews.

## Features
- Automated code analysis for bugs and performance issues.
- Highlights areas for improvement in code style and structure.
- Customizable review criteria based on user input.
- Supports analyzing individual files or entire directories.

## Installation
1. Clone this repository or download the `code_review_assistant.py` file.
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Run the tool from the command line with the following options:

### Analyze a single file
```bash
python code_review_assistant.py --file path/to/your_file.py
```

### Analyze a directory
```bash
python code_review_assistant.py --dir path/to/your_directory
```

### Save the report to a YAML file
```bash
python code_review_assistant.py --file path/to/your_file.py --output report.yaml
```

### Provide custom review criteria
```bash
python code_review_assistant.py --file path/to/your_file.py --criteria "Focus on security and performance."
```

## Requirements
- Python 3.8+
- `openai==0.27.8`
- `rich==13.5.2`
- `pyyaml==6.0`

## Example
Given a Python file `example.py`:

```python
x = 1
def add(a, b):
    return a + b

print(add(x, 2))
```

Run the following command:
```bash
python code_review_assistant.py --file example.py
```

Output:
```
+------------------+--------------------------+
| File             | Review                  |
+------------------+--------------------------+
| example.py       | This is a mock review.  |
+------------------+--------------------------+
```

## Testing
To run the tests, use pytest:
```bash
pytest test_code_review_assistant.py
```

The tests include mocking of the OpenAI API and ensure the tool behaves as expected in various scenarios.

## License
This project is licensed under the MIT License.