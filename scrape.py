from selenium.webdriver import Remote, ChromeOptions
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
CHROME_DRIVER_ENDPOINT = os.getenv("CHROME_DRIVER_URL")

def fetch_website_content(url):
    """
    Connects to a remote Selenium WebDriver instance and fetches the HTML content of the specified webpage.
    """
    if not CHROME_DRIVER_ENDPOINT:
        print("CHROME_DRIVER_URL is not set in the environment variables.")
        return None

    print("Attempting to connect to the remote browser...")

    # Initialize the Chrome options for the WebDriver
    options = ChromeOptions()
    options.add_argument("--headless")  # Run the browser in headless mode (without GUI)
    
    try:
        # Open a remote browser instance using the WebDriver URL
        with Remote(command_executor=CHROME_DRIVER_ENDPOINT, options=options) as browser:
            browser.get(url)
            print("Page loaded successfully. Scraping content...")
            
            # Extract the page's HTML source
            return browser.page_source
            
    except Exception as e:
        print(f"Error during scraping: {e}")
        return None

def get_cleaned_body_content(html_content):
    """
    Extracts and cleans the body section of the given HTML content.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    body = soup.body
    return body.get_text(separator="\n") if body else ""

def split_content_chunks(content, chunk_size=6000):
    """
    Splits large content into smaller, manageable chunks.
    """
    return [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

