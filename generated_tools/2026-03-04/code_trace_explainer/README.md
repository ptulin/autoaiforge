# Code Trace Explainer

## Description

Code Trace Explainer is a Python utility that takes code execution traces in JSON format and dynamically generates a detailed explanation of the trace. It uses OpenAI's GPT model to provide additional insights into the code flow, variable states, and potential logic issues, making it ideal for debugging complex or unfamiliar codebases.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd code_trace_explainer
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the script with the following command:

```bash
python code_trace_explainer.py --tracefile <path_to_trace_file>
```

- `--tracefile`: Path to the JSON file containing the code execution trace.

### Example

Given a `trace.json` file with the following content:

```json
{
  "trace": [
    {
      "function": "my_function",
      "line": 10,
      "variables": {"x": 5, "y": 10}
    },
    {
      "function": "another_function",
      "line": 20,
      "variables": {"z": 15}
    }
  ]
}
```

Run the tool:

```bash
python code_trace_explainer.py --tracefile trace.json
```

Output:

```
Trace Analysis:
Function: my_function, Line: 10
Variables:
  x: 5
  y: 10

Function: another_function, Line: 20
Variables:
  z: 15

AI Insights:
<AI-generated insights>
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_code_trace_explainer.py
```

The tests include:
- Verifying the `analyze_trace` function.
- Mocking OpenAI API calls to test `generate_ai_insights`.
- Handling errors from the OpenAI API.

## Requirements

- Python 3.7+
- `openai` Python package

Install dependencies using:

```bash
pip install -r requirements.txt
```

## License

This project is licensed under the MIT License.