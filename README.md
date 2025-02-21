# AI Web Scraper

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22.0-FF4B4B)
![Selenium](https://img.shields.io/badge/Selenium-4.10.0-43B02A)
![Gemini](https://img.shields.io/badge/Gemini-API-FF6F61)

An AI-powered web scraper that extracts and parses website content using **Selenium** for web scraping and **Google Gemini** for natural language processing. Built with **Streamlit** for a user-friendly interface.

## 🚀 Features

* **Web Scraping**: Extract website content dynamically using Selenium.
* **AI-Powered Parsing**: Uses Google Gemini to extract meaningful data from the scraped content.
* **User-Friendly Interface**: Built with Streamlit for easy interaction.
* **Dynamic Waiting**: Ensures the page is fully loaded before scraping.
* **Chunked Processing**: Splits large content into manageable chunks for efficient parsing.
* **Structured Output**: Returns parsed results in JSON format for easy integration.

## 📸 Screenshots

<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20165537.png" alt="Screenshot 1" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20172612.png" alt="Screenshot 2" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20132012.png" alt="Screenshot 3" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20164254.png" alt="Screenshot 4" width="700"/>
<img src="https://github.com/Tileni97/AI-Web-Scraper/blob/Tileni97-screens/Screenshot%202024-11-20%20131851.png" alt="Screenshot 5" width="700"/>

## 🛠 Installation

1. **Clone the repository**:
```bash
git clone https://github.com/your-username/ai-web-scraper.git
cd ai-web-scraper
```

2. **Set up a virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
   * Create a `.env` file in the root directory
   * Add your Google Gemini API key:
```plaintext
GOOGLE_API_KEY=your_gemini_api_key
```

## ▶️ Usage

1. Run the application:
```bash
streamlit run main.py
```

2. Enter a website URL in the input field and click **Scrape Website**
3. View the scraped content in the **expandable DOM Content** section
4. Describe what you want to parse (e.g., *"Extract all projects"*) and click **Parse Content**
5. View the parsed results in a table or **download them as a JSON file**

## 💡 Applications

This AI-powered web scraper can be used for:

* **Competitive Research**: Analyze competitor websites and extract key insights
* **Market Analysis**: Gather data from various e-commerce websites
* **Content Aggregation**: Scrape and organize articles, blog posts, or news updates
* **Data Extraction**: Collect specific information from government or business directories

## 🤔 Why I Built This

Finding structured and relevant information from websites can be **time-consuming**. This project automates the process and leverages **AI-powered parsing** to extract meaningful data with minimal effort.

## 📜 License

This project is licensed under the **MIT License** – feel free to use and modify it!

## 👨‍💻 Author

Built with ❤️ by **Tileni**

📧 Contact: your.email@example.com
🔗 GitHub: [Tileni97](https://github.com/Tileni97)

---

**✅ Final Notes**
* Make sure to replace `your-username` and `your.email@example.com` with your actual details
* Add a `LICENSE` file if you haven't already
* Push the `README.md` to your GitHub repository