# Content Guardrail Builder

Content Guardrail Builder is a Python library designed to help AI developers build customizable safety filters for their AI agents. It supports defining rules for detecting and mitigating harmful or offensive content based on keywords, regular expressions, and machine learning models. This tool ensures safer AI outputs by providing modular and extensible filtering capabilities.

## Features

- **Keyword Filtering**: Detect and redact specific keywords from content.
- **Regex Filtering**: Use regular expressions to identify and redact patterns in content.
- **Machine Learning Filtering**: Train and use a machine learning model to classify and filter harmful content.

## Installation

Install the required dependencies using pip:

```bash
pip install pyyaml regex scikit-learn
```

## Usage

Run the tool from the command line:

```bash
python content_guardrail_builder.py --config <path_to_config.yaml> --content <path_to_content.txt>
```

### Configuration File

The configuration file should be in YAML format and can include the following fields:

- `keywords`: A list of keywords to filter.
- `regex_patterns`: A list of regular expressions to filter.
- `ml_model`: (Optional) Configuration for a machine learning model, including training data and labels.

Example:

```yaml
keywords:
  - badword
regex_patterns:
  - "\\bbad\\b"
ml_model:
  training_data:
    - "This is bad"
    - "This is good"
  labels:
    - 1
    - 0
```

## Testing

Run the tests using pytest:

```bash
pytest test_content_guardrail_builder.py
```

The tests include:

- Loading configuration files.
- Filtering content based on keywords and regex patterns.
- Handling cases where the ML model is not provided.

## Limitations

- The tool does not include a pre-trained machine learning model. Users must provide their own training data and labels.
- The `spacy` dependency has been removed to simplify the setup process.

## License

This project is licensed under the MIT License.