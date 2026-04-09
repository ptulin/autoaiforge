# Browser AI Orchestrator

Browser AI Orchestrator is an automation library that simplifies AI-driven browser automation by providing a secure and developer-friendly wrapper around Selenium. It allows AI models to control browsers in a structured manner with built-in safeguards to prevent unsafe or unintended actions. This tool is ideal for tasks such as web scraping, form filling, and automated testing.

## Features

- Open a URL in a browser
- Click elements using CSS selectors
- Fill form fields with specified values
- Run in headless mode for automation without a visible browser
- Logs actions and errors to a file for debugging

## Installation

Install the required dependencies using pip:

```bash
pip install selenium loguru
```

## Usage

Run the script from the command line with the following options:

```bash
python browser_ai_orchestrator.py --url "https://example.com" --click "#button" --fill "#input" "value" --headless
```

### Arguments

- `--url`: The URL to open in the browser.
- `--click`: The CSS selector of the element to click.
- `--fill`: A pair of arguments specifying the CSS selector and the value to fill in a form field.
- `--headless`: Run the browser in headless mode.

## Testing

Run the tests using `pytest`:

```bash
pytest test_browser_ai_orchestrator.py
```

The tests use `unittest.mock` to mock external dependencies, ensuring they do not require network access or a real browser.

## License

This project is licensed under the MIT License.