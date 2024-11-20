from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
from bs4 import BeautifulSoup
import praw
import json
from dotenv import load_dotenv
import os

class SocialScraper:
    def __init__(self):
        load_dotenv()
        self.fb_email = os.getenv('FACEBOOK_EMAIL')
        self.fb_password = os.getenv('FACEBOOK_PASSWORD')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_user_agent = os.getenv('REDDIT_USER_AGENT')

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def facebook_login(self, driver):
        try:
            driver.get("https://www.facebook.com")
            
            try:
                cookie_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "[data-cookiebanner='accept_button']"))
                )
                cookie_button.click()
            except:
                pass

            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "email"))
            )
            email_field.send_keys(self.fb_email)

            password_field = driver.find_element(By.ID, "pass")
            password_field.send_keys(self.fb_password)

            login_button = driver.find_element(By.NAME, "login")
            login_button.click()

            time.sleep(5)
            return True
            
        except Exception as e:
            print(f"Facebook login failed: {str(e)}")
            return False

    def scrape_facebook_group(self, group_url, num_posts=10):
        driver = self.setup_driver()
        posts = []

        try:
            if not self.facebook_login(driver):
                return []

            driver.get(group_url)
            time.sleep(5)

            for _ in range(num_posts // 5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            post_elements = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='article']"))
            )

            content_selectors = [
                "div[dir='auto'] span",
                "div.x1iorvi4 span",
                "div.x1lliihq span",
                "div[data-ad-preview='message']",
                "div.xdj266r",
                "span.x193iq5w",
                "div.x1y1aw1k div",
                "div.x1lliihq"
            ]

            for post in post_elements[:num_posts]:
                try:
                    post_text = ""
                    for selector in content_selectors:
                        try:
                            elements = post.find_elements(By.CSS_SELECTOR, selector)
                            texts = [el.text for el in elements if el.text.strip()]
                            if texts:
                                post_text = "\n".join(texts)
                                break
                        except:
                            continue

                    if not post_text:
                        continue

                    price_pattern = r'(?:N\$|NAD)\s*[\d,]+(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:N\$|NAD)'
                    price_match = re.search(price_pattern, post_text)
                    price = price_match.group(0) if price_match else None

                    timestamp = None
                    try:
                        time_elements = post.find_elements(By.CSS_SELECTOR, "a[href*='/posts/'] span")
                        for element in time_elements:
                            if element.text and not element.text.isspace():
                                timestamp = element.text
                                break
                    except:
                        pass

                    posts.append({
                        "content": post_text,
                        "price": price,
                        "timestamp": timestamp
                    })

                except Exception as e:
                    print(f"Error extracting post: {str(e)}")
                    continue

        except Exception as e:
            print(f"Error scraping Facebook group: {str(e)}")

        finally:
            driver.quit()

        return posts

    def scrape_reddit(self, subreddit_name, search_query=None, limit=10):
        try:
            reddit = praw.Reddit(
                client_id=self.reddit_client_id,
                client_secret=self.reddit_client_secret,
                user_agent=self.reddit_user_agent
            )

            subreddit = reddit.subreddit(subreddit_name)
            posts = []

            submissions = subreddit.search(search_query, limit=limit) if search_query else subreddit.new(limit=limit)

            for submission in submissions:
                post_data = {
                    "title": submission.title,
                    "content": submission.selftext,
                    "url": f"https://reddit.com{submission.permalink}",
                    "score": submission.score,
                    "created_utc": submission.created_utc,
                    "num_comments": submission.num_comments,
                    "author": str(submission.author),
                }

                submission.comments.replace_more(limit=0)
                comments = []
                for comment in submission.comments[:5]:
                    comments.append({
                        "author": str(comment.author),
                        "body": comment.body,
                        "score": comment.score
                    })
                post_data["top_comments"] = comments
                posts.append(post_data)

            return posts

        except Exception as e:
            print(f"Error scraping Reddit: {str(e)}")
            return []