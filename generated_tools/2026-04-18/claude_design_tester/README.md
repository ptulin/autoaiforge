# Claude Design Tester

Claude Design Tester is a Python-based utility that validates UI/UX designs generated via Claude Design. It simulates user interactions and provides detailed reports on accessibility, usability, and functionality.

## Features
- Simulates user interactions to test generated designs.
- Provides accessibility and usability reports.
- Integrates seamlessly with testing pipelines.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd claude_design_tester
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool with the following command:

```bash
python claude_design_tester.py --url <URL_OR_FILE_PATH> --report <OUTPUT_REPORT_PATH>
```

### Example

```bash
python claude_design_tester.py --url http://localhost:5000 --report output.json
```

## Testing

To run the tests, use `pytest`:

```bash
pytest test_claude_design_tester.py
```

## Requirements
- Python 3.8+
- Selenium
- Pytest
- Requests

## License
This project is licensed under the MIT License.
