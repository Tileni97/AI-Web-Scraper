import streamlit as st
from typing import List, Optional
from dataclasses import dataclass
from tenacity import retry, stop_after_attempt, wait_exponential
import logging
from scraper import WebScraper
from parser import ContentParser
from models import ScrapingResult
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WebScraperApp:
    def __init__(self):
        self.initialize_session_state()
        self.scraper = WebScraper()
        self.parser = ContentParser()

    def initialize_session_state(self):
        """Initialize session state variables"""
        if "dom_content" not in st.session_state:
            st.session_state.dom_content = None
        if "scraping_history" not in st.session_state:
            st.session_state.scraping_history = []

    def render_ui(self):
        """Render the main application UI"""
        st.title("AI Web Scraper")

        # Add a sidebar with options
        with st.sidebar:
            st.header("Settings")
            self.chunk_size = st.slider("Content Chunk Size", 1000, 10000, 6000)
            self.overlap = st.slider("Chunk Overlap", 0, 500, 200)
            self.retry_attempts = st.slider("Retry Attempts", 1, 5, 3)

        # Main content area
        url = st.text_input(
            "Enter Website URL", help="Enter the full URL including http:// or https://"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Scrape Website", type="primary"):
                self.handle_scraping(url)

        with col2:
            if st.button("Clear History"):
                self.clear_history()

        self.render_content_section()

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def handle_scraping(self, url: str):
        """Handle the website scraping process with error handling"""
        if not url:
            st.error("Please enter a valid URL")
            return

        try:
            with st.spinner("Scraping website..."):
                progress_bar = st.progress(0)
                result = self.scraper.scrape(url)
                progress_bar.progress(100)

                if result.success:
                    st.session_state.dom_content = result.cleaned_content
                    st.success("Website scraped successfully!")

                    # Store in history
                    st.session_state.scraping_history.append(
                        {"url": url, "content_length": len(result.cleaned_content)}
                    )
                else:
                    st.error(f"Failed to scrape website: {result.error}")

        except Exception as e:
            logger.error(f"Error scraping website: {str(e)}")
            st.error(f"An error occurred: {str(e)}")

    def render_content_section(self):
        """Render the content viewing and parsing section"""
        if st.session_state.dom_content:
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", st.session_state.dom_content, height=300)

            st.subheader("Parse Content")
            parse_description = st.text_area(
                "Describe what you want to parse",
                help="Describe the specific information you want to extract from the content",
            )

            if st.button("Parse Content", type="primary"):
                self.handle_parsing(parse_description)

    def handle_parsing(self, parse_description: str):
        """Handle the content parsing process"""
        if not parse_description:
            st.warning("Please provide a description of what to parse")
            return

        try:
            with st.spinner("Parsing content..."):
                # Hardcoded query for testing
                test_query = "Extract all projects mentioned in the content."
                parsed_result = self.parser.parse(
                    st.session_state.dom_content, test_query
                )

                st.subheader("Parsed Result")

                # Display the parsed result as a table
                if parsed_result.get("data"):
                    st.table(parsed_result["data"])
                else:
                    st.info("No relevant information found.")

                # Add download button for results
                st.download_button(
                    "Download Results",
                    json.dumps(parsed_result, indent=2),
                    "parsed_results.json",
                    "application/json",
                )

        except Exception as e:
            logger.error(f"Error parsing content: {str(e)}")
            st.error(f"An error occurred while parsing: {str(e)}")

    def clear_history(self):
        """Clear the scraping history"""
        st.session_state.scraping_history = []
        st.session_state.dom_content = None
        st.success("History cleared!")


if __name__ == "__main__":
    app = WebScraperApp()
    app.render_ui()
