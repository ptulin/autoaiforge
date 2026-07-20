import argparse
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import numpy as np

def analyze_response_time(response_time):
    """Adjust scrape delay based on response time."""
    if response_time < 1:
        return 1  # Fast response, scrape more frequently
    elif response_time < 3:
        return 2  # Moderate response, scrape less frequently
    else:
        return 5  # Slow response, scrape infrequently

def fetch_html_with_requests(url, headers):
    """Fetch HTML content using requests."""
    try:
        start_time = time.time()
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        response_time = time.time() - start_time
        return response.text, response_time
    except requests.RequestException as e:
        print(f"Error fetching URL with requests: {e}")
        return None, None

def fetch_html_with_selenium(url, browser_type):
    """Fetch HTML content using Selenium for JavaScript-heavy websites."""
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        if browser_type == 'chrome':
            service = Service()  # Default ChromeDriver service
            driver = webdriver.Chrome(service=service, options=options)
        else:
            raise ValueError("Unsupported browser type")

        start_time = time.time()
        driver.get(url)
        time.sleep(2)  # Allow JavaScript to load
        response_time = time.time() - start_time
        html = driver.page_source
        driver.quit()
        return html, response_time
    except Exception as e:
        print(f"Error fetching URL with Selenium: {e}")
        return None, None

def scrape_data(url, output, browser_type):
    """Main scraping function."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    html, response_time = fetch_html_with_requests(url, headers)

    if html is None:
        print("Falling back to Selenium...")
        html, response_time = fetch_html_with_selenium(url, browser_type)

    if html is None:
        print("Failed to fetch HTML content.")
        return

    delay = analyze_response_time(response_time)
    print(f"Adjusting scrape delay to {delay} seconds based on response time.")

    soup = BeautifulSoup(html, 'html.parser')
    data = {
        'title': soup.title.string if soup.title else None,
        'headings': [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2', 'h3'])],
        'links': [a['href'] for a in soup.find_all('a', href=True)]
    }

    with open(output, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Scraped data saved to {output}")

def main():
    parser = argparse.ArgumentParser(description="Adaptive Web Scraper")
    parser.add_argument('--url', required=True, help="Target URL to scrape")
    parser.add_argument('--output', required=True, help="Output file for scraped data (JSON format)")
    parser.add_argument('--browser', default='chrome', choices=['chrome'], help="Browser type for Selenium (default: chrome)")

    args = parser.parse_args()

    scrape_data(args.url, args.output, args.browser)

if __name__ == "__main__":
    main()