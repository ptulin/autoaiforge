from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
from loguru import logger
import time

class BrowserAI:
    def __init__(self, headless=True, timeout=10):
        """
        Initializes the BrowserAI instance.

        :param headless: Whether to run the browser in headless mode.
        :param timeout: Default timeout for browser actions in seconds.
        """
        self.timeout = timeout
        self.headless = headless
        self.driver = None

        logger.add("browser_ai.log", rotation="1 MB", level="INFO")

    def _initialize_driver(self):
        """
        Initializes the Selenium WebDriver.
        """
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")

            service = Service()
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.set_page_load_timeout(self.timeout)
            logger.info("WebDriver initialized.")
        except WebDriverException as e:
            logger.error(f"Failed to initialize WebDriver: {e}")
            raise

    def open_url(self, url):
        """
        Opens a URL in the browser.

        :param url: The URL to open.
        """
        if not self.driver:
            self._initialize_driver()

        try:
            self.driver.get(url)
            logger.info(f"Opened URL: {url}")
        except WebDriverException as e:
            logger.error(f"Failed to open URL {url}: {e}")
            raise

    def click_element(self, css_selector):
        """
        Clicks an element identified by a CSS selector.

        :param css_selector: The CSS selector of the element to click.
        """
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            element.click()
            logger.info(f"Clicked element: {css_selector}")
        except WebDriverException as e:
            logger.error(f"Failed to click element {css_selector}: {e}")
            raise

    def fill_form(self, css_selector, value):
        """
        Fills a form field identified by a CSS selector.

        :param css_selector: The CSS selector of the form field.
        :param value: The value to input into the form field.
        """
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, css_selector)
            element.clear()
            element.send_keys(value)
            logger.info(f"Filled form field {css_selector} with value: {value}")
        except WebDriverException as e:
            logger.error(f"Failed to fill form field {css_selector}: {e}")
            raise

    def quit(self):
        """
        Closes the browser and quits the WebDriver.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
            logger.info("Browser closed and WebDriver quit.")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Browser AI Orchestrator")
    parser.add_argument("--url", type=str, help="URL to open in the browser.")
    parser.add_argument("--click", type=str, help="CSS selector of element to click.")
    parser.add_argument("--fill", nargs=2, metavar=("CSS_SELECTOR", "VALUE"), help="CSS selector and value to fill in a form.")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode.")

    args = parser.parse_args()

    ai = BrowserAI(headless=args.headless)

    try:
        if args.url:
            ai.open_url(args.url)
        if args.click:
            ai.click_element(args.click)
        if args.fill:
            ai.fill_form(args.fill[0], args.fill[1])
    finally:
        ai.quit()
