# Toxic Content Tester

## Description
The `toxic_content_tester` is a CLI tool designed to help developers evaluate the outputs of AI agents against predefined safety filters. It identifies harmful or offensive content and generates a detailed report that highlights potential vulnerabilities in the AI system.

## Features
- Load AI outputs from a CSV file.
- Load safety rules from a JSON file.
- Evaluate AI outputs against the safety rules.
- Generate a detailed report in JSON or HTML format.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd toxic_content_tester
   ```

2. Install the required dependencies:
   ```bash
   pip install pandas
   ```

## Usage

Run the tool using the following command:

```bash
python toxic_content_tester.py --outputs <path_to_outputs_csv> --rules <path_to_rules_json> --report <path_to_report> --format <json_or_html>
```

### Arguments
- `--outputs`: Path to the CSV file containing AI outputs. The file should have columns `id` and `content`.
- `--rules`: Path to the JSON file containing safety rules. The file should be a list of objects with `keyword` and `description` fields.
- `--report`: Path to save the generated report.
- `--format`: Format of the report. Can be either `json` or `html`. Default is `json`.

### Example

```bash
python toxic_content_tester.py --outputs outputs.csv --rules rules.json --report report.json --format json
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_toxic_content_tester.py
```

Ensure all tests pass successfully.

## License
This project is licensed under the MIT License.