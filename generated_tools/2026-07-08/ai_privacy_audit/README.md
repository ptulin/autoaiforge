# AI Privacy Audit Tool

## Description
The AI Privacy Audit Tool scans AI system logs or outputs for sensitive data exposure, including private user data or confidential information. It performs advanced pattern matching and semantic checks to identify leaks that generic tools might miss.

## Installation

1. Install the required Python packages:

```bash
pip install regex spacy
```

2. Download the spaCy language model:

```bash
python -m spacy download en_core_web_sm
```

## Usage

Run the tool from the command line:

```bash
python ai_privacy_audit.py --logfile <path_to_log_file> --pii-check
```

### Arguments

- `--logfile`: Path to the log file to scan.
- `--pii-check`: Enable PII detection.

## Testing

Run the tests using pytest:

```bash
pytest test_ai_privacy_audit.py
```

## License
MIT License