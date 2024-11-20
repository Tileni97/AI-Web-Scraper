# scrape.py
from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import time
import re

# Load environment variables
load_dotenv()
SBR_WEBDRIVER = os.getenv("SBR_WEBDRIVER")

def is_amazon_url(url):
    """Check if the URL is from Amazon"""
    return 'amazon' in url.lower()

def scrape_website(url):
    """
    Scrape website content using SBR WebDriver
    Optimized for Amazon and other e-commerce sites
    """
    print(f"SBR_WEBDRIVER: {SBR_WEBDRIVER}")
    
    try:
        # Setup ChromeOptions
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        # Add headers to appear more like a real browser
        options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
        
        # Setup connection
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, "goog", "chrome")
        
        # Create driver with enhanced options
        with Remote(sbr_connection, options=options) as driver:
            # Navigate to the URL
            driver.get(url)
            
            if is_amazon_url(url):
                # Wait for specific Amazon elements
                print("Detected Amazon URL, waiting for product elements...")
                try:
                    # Wait for captcha to solve if present
                    solve_res = driver.execute(
                        "executeCdpCommand",
                        {
                            "cmd": "Captcha.waitForSolve",
                            "params": {"detectTimeout": 10000},
                        },
                    )
                    print("Captcha solve status:", solve_res["value"]["status"])
                except:
                    print("No captcha detected or captcha handling failed")
                
                # Wait for common Amazon elements
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Add additional wait time for dynamic content
                time.sleep(3)
            
            # Get the page source
            html = driver.page_source
            print("Successfully retrieved page content")
            return html
            
    except Exception as e:
        raise Exception(f"Failed to scrape website: {str(e)}")

def extract_body_content(html_content):
    """
    Extract and clean body content, with special handling for e-commerce sites
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove unnecessary elements
        for element in soup.find_all(['script', 'style', 'iframe', 'noscript', 'header', 'footer']):
            element.decompose()
        
        # Special handling for Amazon content
        if soup.find(id='dp') or soup.find(id='productTitle'):  # Amazon product page detection
            important_elements = []
            
            # Product title
            product_title = soup.find(id='productTitle')
            if product_title:
                important_elements.append(product_title.get_text(strip=True))
            
            # Price
            price_elements = soup.find_all(class_=re.compile(r'price|a-price'))
            for element in price_elements:
                if element.get_text(strip=True):
                    important_elements.append(element.get_text(strip=True))
            
            # Product description
            description = soup.find(id='productDescription')
            if description:
                important_elements.append(description.get_text(strip=True))
            
            # Features
            feature_bullets = soup.find(id='feature-bullets')
            if feature_bullets:
                important_elements.append(feature_bullets.get_text(strip=True))
            
            # Technical details
            tech_details = soup.find(id='productDetails_techSpec_section_1')
            if tech_details:
                important_elements.append(tech_details.get_text(strip=True))
            
            return '\n'.join(important_elements)
        
        # Default handling for non-Amazon pages
        body_content = soup.body
        if body_content:
            return str(body_content)
        return ""
        
    except Exception as e:
        raise Exception(f"Failed to extract body content: {str(e)}")

def clean_body_content(body_content):
    """
    Clean and structure the body content
    """
    try:
        soup = BeautifulSoup(body_content, 'html.parser')
        
        # Get text and clean it
        text = soup.get_text(separator=' ')
        
        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Remove multiple spaces and normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    except Exception as e:
        raise Exception(f"Failed to clean body content: {str(e)}")

def split_dom_content(dom_content, max_length=6000):
    """
    Split content into chunks, ensuring important information stays together
    """
    # If content contains product information, adjust splitting to keep related info together
    if 'Product Description' in dom_content or 'Technical Details' in dom_content:
        # Split on major sections while preserving context
        sections = re.split(r'(?=Product Description|Technical Details|Customer Reviews)', dom_content)
        chunks = []
        current_chunk = ""
        
        for section in sections:
            if len(current_chunk) + len(section) <= max_length:
                current_chunk += section
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = section
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    # Default splitting for non-product pages
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]