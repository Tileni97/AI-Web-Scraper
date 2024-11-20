# AI Web Scraper

An advanced AI-powered web scraper that combines web scraping technologies with Google's Gemini AI to extract specific information from websites based on user prompts.

## Key Features
- Dynamic web scraping with Selenium
- Intelligent content parsing with BeautifulSoup
- AI-powered extraction using Google's Gemini AI
- Multi-platform support (Websites, Facebook Groups, Reddit)
- Customizable analysis options
- Data export in CSV/JSON formats

## Technologies
- Python
- Streamlit
- Selenium WebDriver
- BeautifulSoup4
- Google Gemini AI
- Pandas/Plotly
## Screenshots
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20165537.png" alt="CryptoTracker Screenshot 2" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20172612.png" alt="CryptoTracker Screenshot 2" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20132012.png" alt="CryptoTracker Screenshot 2" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20164254.png" alt="CryptoTracker Screenshot 2" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20131851.png" alt="CryptoTracker Screenshot 2" width="700"/>

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```plaintext
GOOGLE_API_KEY=your_gemini_api_key
FACEBOOK_EMAIL=your_facebook_email
FACEBOOK_PASSWORD=your_facebook_password
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USER_AGENT=your_app_name
```

3. Run the application:
```bash
streamlit run main.py
```

## Usage

Select the platform: Choose from Website, Facebook Groups, or Reddit.
Enter parameters: Input a URL or search criteria.
Select analysis type:
Product Information
Price Comparison
Feature Comparison
Review Analysis
Technical Specifications
Custom Analysis
View results: Let AI extract and present insights tailored to your requirements.

## Applications

Market Research: Gather data to understand trends and competitors.
Price Monitoring: Track product prices across platforms.
Content Aggregation: Compile information from multiple sources.
Customer Insights: Analyze reviews and customer sentiments.
Product Analysis: Compare features and specifications.
Future Improvements
Enhance AI accuracy for better contextual understanding.
Add support for additional platforms and data export formats.
Refine the user interface for an improved experience.

## Why I Built This

Finding rental apartments in Windhoek often involves scouring Facebook posts, which can be tedious and inefficient. I built this tool to simplify data extraction and analysis, making my search more manageable. While it’s still a work in progress, it’s already proven helpful, and I hope it can evolve into a more comprehensive solution.

## License

This project is licensed under the MIT License.

## Author

Built with ❤️ by Tileni

