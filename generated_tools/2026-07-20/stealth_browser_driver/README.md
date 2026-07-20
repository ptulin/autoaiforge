# Stealth Browser Driver

## Overview
The Stealth Browser Driver is a Python tool designed to provide a stealthy browser automation environment. It mimics human-like browsing patterns using real web browsers and includes anti-detection techniques such as randomized user-agent headers, dynamic time delays, and browser fingerprint masking.

## Features
- Randomized user-agent headers
- Headless browser operation
- Dynamic time delays to simulate human behavior
- Browser fingerprint masking
- Custom interaction scripts

## Installation

1. Install the required Python packages:

```bash
pip install selenium fake-useragent
```

2. Ensure you have the appropriate web driver installed for Chrome. For example, you can download the ChromeDriver from [https://sites.google.com/chromium.org/driver/](https://sites.google.com/chromium.org/driver/).

## Usage

Run the script with the following arguments:

```bash
python stealth_browser_driver.py --url <URL> --browser chrome [--script <SCRIPT_PATH>]
```

### Arguments
- `--url`: The URL to visit.
- `--browser`: The browser to use (currently only Chrome is supported).
- `--script`: (Optional) Path to a Python script for custom interactions.

### Example

```bash
python stealth_browser_driver.py --url https://example.com --browser chrome --script interaction_script.py
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Then execute the tests:

```bash
pytest test_stealth_browser_driver.py
```

## License
This project is licensed under the MIT License.