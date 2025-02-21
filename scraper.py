from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from typing import List
import os
import random
from models import ScrapingResult


class WebScraper:
    def __init__(self):
        # Initialize Chrome options
        self.options = Options()
        self.options.add_argument("--headless=new")  # Updated headless argument
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-software-rasterizer")

        # Rotate user agents to avoid detection
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15",
        ]
        self.options.add_argument(f"user-agent={random.choice(self.user_agents)}")

        # Set up Chrome service
        self.service = Service(ChromeDriverManager().install())

    def scrape(self, url: str) -> ScrapingResult:
        """Scrape website content with error handling"""
        try:
            html_content = self._fetch_page_content(url)
            body_content = self._extract_body_content(html_content)
            cleaned_content = self._clean_content(body_content)

            # Log the cleaned content for debugging
            print("Cleaned Content:", cleaned_content)

            return ScrapingResult(
                raw_content=html_content, cleaned_content=cleaned_content, success=True
            )

        except Exception as e:
            return ScrapingResult(
                raw_content="", cleaned_content="", success=False, error=str(e)
            )

    def _fetch_page_content(self, url: str) -> str:
        """Fetch page content using local Chrome WebDriver"""
        driver = webdriver.Chrome(service=self.service, options=self.options)
        try:
            driver.get(url)

            # Wait for the page to load completely
            wait = WebDriverWait(driver, 20)
            wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            return driver.page_source
        finally:
            driver.quit()

    def _extract_body_content(self, html_content: str) -> str:
        """Extract body content from HTML"""
        soup = BeautifulSoup(html_content, "html.parser")
        body = soup.body
        return str(body) if body else ""

    def _clean_content(self, content: str) -> str:
        """Clean the extracted content"""
        soup = BeautifulSoup(content, "html.parser")

        # Remove scripts and styles
        for element in soup(["script", "style", "meta", "link"]):
            element.decompose()

        # Get text with better formatting
        lines = soup.get_text(separator="\n").splitlines()
        cleaned_lines = [line.strip() for line in lines if line.strip()]
        return "\n".join(cleaned_lines)
