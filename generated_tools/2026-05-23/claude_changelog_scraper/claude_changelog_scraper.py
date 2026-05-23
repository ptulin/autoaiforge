import argparse
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_updates(url):
    """Fetch the HTML content from the given URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise RuntimeError(f"Error fetching updates from {url}: {e}")

def parse_updates(html_content, keywords=None, date_range=None):
    """Parse the HTML content and extract updates based on filters."""
    soup = BeautifulSoup(html_content, 'html.parser')
    updates = []

    # Example: Assuming updates are in <div class="update"> elements
    for update_div in soup.find_all('div', class_='update'):
        title = update_div.find('h2').get_text(strip=True) if update_div.find('h2') else 'No Title'
        date_text = update_div.find('time').get_text(strip=True) if update_div.find('time') else 'Unknown Date'
        description = update_div.find('p').get_text(strip=True) if update_div.find('p') else 'No Description'

        try:
            date = datetime.strptime(date_text, '%Y-%m-%d')
        except ValueError:
            date = None

        if date_range and date:
            start_date, end_date = date_range
            if not (start_date <= date <= end_date):
                continue

        if keywords:
            if not any(keyword.lower() in (title + description).lower() for keyword in keywords):
                continue

        updates.append({
            'title': title,
            'date': date_text,
            'description': description
        })

    return updates

def save_updates(updates, output_format, output_file):
    """Save updates to a file or print to stdout."""
    if output_format == 'json':
        output_content = json.dumps(updates, indent=4)
    else:
        output_content = '\n\n'.join(f"Title: {u['title']}\nDate: {u['date']}\nDescription: {u['description']}" for u in updates)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(output_content)
    else:
        print(output_content)

def main():
    parser = argparse.ArgumentParser(description="Claude Changelog Scraper")
    parser.add_argument('--url', required=True, help="URL to scrape updates from")
    parser.add_argument('--filter', help="Comma-separated keywords to filter updates")
    parser.add_argument('--date-range', help="Date range to filter updates (format: YYYY-MM-DD,YYYY-MM-DD)")
    parser.add_argument('--output', help="Output file to save results (default: stdout)")
    parser.add_argument('--format', choices=['text', 'json'], default='text', help="Output format (default: text)")

    args = parser.parse_args()

    keywords = args.filter.split(',') if args.filter else None
    date_range = None
    if args.date_range:
        try:
            start_date, end_date = args.date_range.split(',')
            date_range = (
                datetime.strptime(start_date, '%Y-%m-%d'),
                datetime.strptime(end_date, '%Y-%m-%d')
            )
        except ValueError:
            parser.error("Invalid date range format. Use YYYY-MM-DD,YYYY-MM-DD")

    try:
        html_content = fetch_updates(args.url)
        updates = parse_updates(html_content, keywords, date_range)
        save_updates(updates, args.format, args.output)
    except RuntimeError as e:
        print(e)

if __name__ == '__main__':
    main()