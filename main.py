# main.py
import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_gemini
from social_scraper import SocialScraper
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json

load_dotenv()

st.set_page_config(
    page_title="AI Web Scraper",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .stCard {
            border-radius: 1rem;
            padding: 1.5rem;
            background-color: #f8f9fa;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1rem;
        }
        .analysis-option {
            padding: 1rem;
            border: 1px solid #ddd;
            border-radius: 0.5rem;
            margin: 0.5rem 0;
        }
        .analysis-option:hover {
            background-color: #f5f5f5;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar section
with st.sidebar:
    st.title("🔍 Scraping Options")
    platform = st.radio("Select Platform", ["Website", "Facebook Group", "Reddit"])

    if platform == "Facebook Group":
        num_posts = st.slider("Number of posts", 5, 50, 10)
        st.markdown("### 🏠 Rental Preferences")
        min_price = st.number_input("Minimum Price (N$)", 0, 50000, 8000)
        max_price = st.number_input("Maximum Price (N$)", 0, 50000, 10000)
        location = st.text_input("Preferred Location", "Windhoek")
        bedrooms = st.selectbox("Bedrooms", ["Any", "1", "2", "3", "4+"])
    elif platform == "Reddit":
        subreddit = st.text_input("Subreddit name (without r/)")
        search_query = st.text_input("Search query (optional)")
        num_posts = st.slider("Number of posts", 5, 100, 25)

    if platform != "Facebook Group":
        st.markdown("---")
        st.title("🔍 Analysis Options")
        analysis_type = st.radio(
            "Choose Analysis Type",
            ["Product Information", "Price Comparison", "Feature Comparison", 
             "Review Analysis", "Technical Specifications", "Custom Analysis"]
        )
        
        st.markdown("### 📊 Analysis Settings")
        if analysis_type == "Price Comparison":
            price_range = st.slider("Price Range ($)", 0, 1000, (0, 500))
            sort_by = st.selectbox("Sort By", ["Price: Low to High", "Price: High to Low"])
        elif analysis_type == "Feature Comparison":
            features = st.multiselect(
                "Select Features to Compare",
                ["Brand", "Model", "Specifications", "Connectivity", "Battery Life", "Compatibility"]
            )
        elif analysis_type == "Review Analysis":
            min_rating = st.slider("Minimum Rating", 1, 5, 3)
            sentiment = st.multiselect("Sentiment", ["Positive", "Negative", "Neutral"])

st.title("🤖 AI Web Scraper")

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Google API Key", type="password")
    if api_key:
        st.session_state.GOOGLE_API_KEY = api_key
else:
    st.session_state.GOOGLE_API_KEY = api_key

col1, col2 = st.columns([3, 1])
with col1:
    if platform == "Website":
        url = st.text_input("🌐 Enter Website URL", placeholder="https://example.com")
    elif platform == "Facebook Group":
        url = st.text_input("🌐 Enter Facebook Group URL", placeholder="https://www.facebook.com/groups/...")
    else:
        url = ""

if st.button("🚀 Start Scraping", key="scrape_button", use_container_width=True):
    if (platform in ["Website", "Facebook Group"] and url) or (platform == "Reddit" and subreddit):
        with st.spinner(f"Scraping {platform}..."):
            try:
                scraper = SocialScraper()
                if platform == "Website":
                    content = scrape_website(url)
                    st.session_state.dom_content = clean_body_content(extract_body_content(content))
                    st.success("Website scraped successfully! 🎉")
                
                elif platform == "Facebook Group":
                    results = scraper.scrape_facebook_group(url, num_posts)
                    if results:
                        st.session_state.dom_content = "\n".join([post["content"] for post in results])
                        df = pd.DataFrame(results)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Posts", len(df))
                        with col2:
                            st.metric("Posts with Content", df['content'].notna().sum())
                        with col3:
                            st.metric("Posts with Prices", df['price'].notna().sum())

                        with st.expander("View Raw Data"):
                            st.dataframe(df[['content', 'price', 'timestamp']], use_container_width=True)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                st.download_button(
                                    "📥 Download as CSV",
                                    df.to_csv(index=False).encode('utf-8'),
                                    "facebook_posts.csv",
                                    "text/csv"
                                )
                            with col2:
                                st.download_button(
                                    "📥 Download as JSON",
                                    json.dumps(results, indent=2),
                                    "facebook_posts.json",
                                    "application/json"
                                )
                        st.success("Successfully scraped Facebook posts! 🎉")
                
                elif platform == "Reddit":
                    results = scraper.scrape_reddit(subreddit, search_query, num_posts)
                    if results:
                        st.session_state.dom_content = "\n".join(
                            [f"Title: {post['title']}\nContent: {post['content']}" for post in results]
                        )
                        df = pd.DataFrame(results)
                        st.dataframe(df[['title', 'content', 'score']], use_container_width=True)
                        st.success("Successfully scraped Reddit posts! 🎉")
                
            except Exception as e:
                st.error(f"❌ Error during scraping: {str(e)}")
    else:
        st.warning("⚠️ Please enter required information")

# Analysis section
if "dom_content" in st.session_state and "GOOGLE_API_KEY" in st.session_state:
    st.markdown("---")
    
    if platform == "Facebook Group":
        prompt = f"""Analyze these rental posts and extract only properties that match:
        - Price range: N${min_price} - N${max_price}
        - Location: {location}
        - Bedrooms: {bedrooms if bedrooms != "Any" else "any number"}

        For each matching property, format as:
        PRICE: [amount in N$]
        LOCATION: [specific area in {location}]
        BEDROOMS: [number]
        BATHROOMS: [number if mentioned]
        CONTACT: [phone/email]
        AVAILABLE: [date if mentioned]
        FEATURES: [key amenities]
        POSTED: [post date]

        Sort results by price (lowest to highest).
        Only include properties with clear pricing information."""
    else:
        if analysis_type == "Custom Analysis":
            prompt = st.text_area("What would you like to analyze?", 
                                placeholder="Describe your analysis...")
        else:
            prompts = {
                "Product Information": """Extract and list all products with their key information:
                    - Product name
                    - Brand
                    - Model
                    - Key features
                    Format as a structured list.""",
                "Price Comparison": f"""Extract and compare prices:
                    - Product name
                    - Price
                    - Any discounts or deals
                    Only include products within price range: ${price_range[0]} - ${price_range[1]}
                    Sort by: {sort_by}""",
                "Feature Comparison": f"""Compare products based on these features: {', '.join(features)}
                    Create a detailed comparison showing differences and similarities.""",
                "Review Analysis": f"""Analyze reviews:
                    - Extract reviews with {min_rating}+ stars
                    - Focus on {', '.join(sentiment)} sentiments
                    - Summarize key points
                    - Identify common praise and complaints""",
                "Technical Specifications": """Extract and compare technical specifications:
                    - Technical details
                    - Performance metrics
                    - Compatibility
                    - Connectivity options"""
            }
            prompt = prompts[analysis_type]

    if st.button("📊 Analyze Content", key="analyze_button"):
        with st.spinner("Analyzing content..."):
            try:
                dom_chunks = split_dom_content(st.session_state.dom_content)
                results = parse_with_gemini(dom_chunks, prompt, st.session_state.GOOGLE_API_KEY)
                
                tab1, tab2 = st.tabs(["📝 Text View", "📊 Structured View"])
                
                with tab1:
                    st.text_area("Results (Click to copy)", value=results, height=300)
                    st.download_button(
                        "📥 Download Results",
                        results,
                        f"analysis_results.txt",
                        "text/plain"
                    )
                
                with tab2:
                    try:
                        lines = [line.strip() for line in results.split('\n') if line.strip()]
                        if lines:
                            df = pd.DataFrame([line.split(':') if ':' in line else [line, ''] 
                                            for line in lines], columns=['Item', 'Details'])
                            st.dataframe(df, use_container_width=True, hide_index=True)
                    except:
                        st.warning("Unable to create structured view for these results")
            
            except Exception as e:
                st.error(f"❌ Error in analysis: {str(e)}")

elif "dom_content" in st.session_state:
    st.warning("⚠️ No Google API key found. Please check your .env file or enter the key manually.")

st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>Built with ❤️ by Tileni using Streamlit and Google's Gemini AI</p>
    </div>
""", unsafe_allow_html=True)