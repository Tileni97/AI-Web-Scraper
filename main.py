import streamlit as st
from scrape import (
    fetch_website_content,
    get_cleaned_body_content,
    split_content_chunks,
)
from parse import process_with_ai

# Set up the Streamlit UI
st.title("AI-Powered Web Scraper")
url_input = st.text_input("Input Website URL")

# Step 1: Scrape and Display Website Data
if st.button("Scrape Website Content"):
    if url_input:
        st.write("Initiating the scraping process...")

        # Perform scraping
        website_dom = fetch_website_content(url_input)
        body_content = get_cleaned_body_content(website_dom)

        # Store the cleaned content in the session state
        st.session_state.cleaned_content = body_content

        # Allow users to view the content in an expandable section
        with st.expander("View Scraped Content"):
            st.text_area("Extracted DOM", body_content, height=300)

# Step 2: Process Extracted Content
if "cleaned_content" in st.session_state:
    parse_request = st.text_area("Describe the Information to Extract")

    if st.button("Process Content"):
        if parse_request:
            st.write("Processing content using AI...")

            # Break content into manageable chunks and analyze
            content_chunks = split_content_chunks(st.session_state.cleaned_content)
            parsed_output = process_with_ai(content_chunks, parse_request)
            st.write(parsed_output)
