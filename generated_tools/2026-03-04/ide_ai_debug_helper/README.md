# IDE AI Debug Helper

## Overview
The IDE AI Debug Helper is a lightweight Python library that integrates with your IDE (VS Code, PyCharm, etc.) to automatically analyze exceptions or runtime errors. When an error occurs, it uses Claude AI to generate insights and fix suggestions, displaying them in the IDE's output window.

## Features
- Automatically captures Python exceptions.
- Sends the exception details to Claude AI for analysis.
- Displays suggestions and insights in the terminal or IDE output window.

## Installation

1. Install the required Python packages:

```bash
pip install openai pygments
```

2. Save the `ide_ai_debug_helper.py` file to your project directory.

## Usage

1. Run the script with your OpenAI API key:

```bash
python ide_ai_debug_helper.py --api-key YOUR_API_KEY
```

2. Once started, the tool will automatically capture and analyze any unhandled exceptions in your Python scripts.

## Testing

The project includes a test suite written with `pytest`. To run the tests:

1. Install `pytest`:

```bash
pip install pytest
```

2. Run the tests:

```bash
pytest test_ide_ai_debug_helper.py
```

All tests are mocked and do not require network access.

## License

This project is licensed under the MIT License.