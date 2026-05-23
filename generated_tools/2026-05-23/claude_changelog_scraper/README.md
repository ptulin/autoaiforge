# Claude Changelog Scraper

## Overview

The Claude Changelog Scraper is a CLI tool that allows developers to scrape the latest updates and changelogs for Claude AI from its official sources or news articles. This tool helps developers stay informed about new features, improvements, and breaking changes without manually sifting through multiple web pages.

## Features

- Fetch updates from a specified URL.
- Filter updates by keywords.
- Filter updates by a date range.
- Save updates to a file in JSON or plain text format, or print them to the console.

## Requirements

The tool requires the following Python packages:

- `requests`
- `beautifulsoup4`

Install the dependencies using pip:

```bash
pip install requests beautifulsoup4
```

## Usage

Run the script using the command line:

```bash
python claude_changelog_scraper.py --url <URL> [--filter <keywords>] [--date-range <start_date,end_date>] [--output <output_file>] [--format <text|json>]
```

### Arguments

- `--url`: The URL to scrape updates from (required).
- `--filter`: Comma-separated keywords to filter updates (optional).
- `--date-range`: Date range to filter updates in the format `YYYY-MM-DD,YYYY-MM-DD` (optional).
- `--output`: Output file to save results (optional, default is to print to stdout).
- `--format`: Output format, either `text` or `json` (optional, default is `text`).

### Example

Fetch updates from a URL and filter by keywords:

```bash
python claude_changelog_scraper.py --url https://example.com --filter performance,bug --date-range 2023-09-01,2023-10-01 --output updates.json --format json
```

## Testing

To run the tests, install `pytest`:

```bash
pip install pytest
```

Run the tests using:

```bash
pytest test_claude_changelog_scraper.py
```

The tests include:

- Verifying successful fetching of updates.
- Handling network errors gracefully.
- Parsing updates with filters for keywords and date ranges.

## License

This project is licensed under the MIT License.