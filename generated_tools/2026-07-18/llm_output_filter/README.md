# LLM Output Filter

LLM Output Filter is a Python tool designed to filter the output of large language models (LLMs). It helps detect and redact potentially harmful or sensitive content before it is displayed, ensuring safe and secure usage of LLMs.

## Features

- **Customizable Filtering Rules**: Define your own filtering rules using regular expressions or load them from a JSON file.
- **Inline Replacement or Output Blocking**: Replace sensitive content inline or block it entirely.
- **Real-Time Analysis**: Processes text with minimal latency, making it suitable for real-time applications.

## Installation

Install the required dependencies using pip:

```bash
pip install transformers==4.33.0
```

## Usage

### As a Library

```python
from llm_output_filter import filter_output

# Example text and rules
text = "My credit card number is 1234-5678-9012-3456."
rules = {
    r"\b\d{4}-\d{4}-\d{4}-\d{4}\b": "[REDACTED]"
}

filtered_text = filter_output(text, rules=rules)
print(filtered_text)  # Output: My credit card number is [REDACTED].
```

### Using CLI

```bash
python llm_output_filter.py "My email is user@example.com." --rules '{"\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b": "[REDACTED]"}'
```

Or with a rules file:

```bash
python llm_output_filter.py "My email is user@example.com." --rules_file rules.json
```

## Example Rules

Here is an example of a JSON rules file:

```json
{
    "\\b\\d{4}-\\d{4}-\\d{4}-\\d{4}\\b": "[REDACTED]",
    "\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{2,}\\b": "[REDACTED]"
}
```

## Testing

Run the tests using pytest:

```bash
pytest test_llm_output_filter.py
```

## License

This project is licensed under the MIT License.