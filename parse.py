# parse.py
import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_gemini(api_key: str = None):
    """Configure Gemini with API key"""
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("Google API key not found. Please check your .env file or provide the key manually.")
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-pro')

def create_prompt(dom_content: str, parse_description: str) -> str:
    """Create analysis prompt for Gemini"""
    return f"""Analyze and extract information from the following text based on the given description.
    
Text content: {dom_content}

Instructions:
1. Focus on this specific request: {parse_description}
2. Extract and structure the relevant information
3. Format the output in a clear, easily readable way
4. If no relevant information is found, indicate this clearly

Provide your analysis:"""

def parse_with_gemini(dom_chunks: List[str], parse_description: str, api_key: str = None) -> str:
    """Parse content using Gemini API"""
    try:
        # Setup Gemini model
        model = setup_gemini(api_key)
        parsed_results = []

        for i, chunk in enumerate(dom_chunks, start=1):
            try:
                prompt = create_prompt(chunk, parse_description)
                
                # Generate response
                response = model.generate_content(prompt)
                
                # Extract and clean the response
                result = response.text.strip()
                if result and result.lower() != "none" and result != "''":
                    parsed_results.append(result)
                    
            except Exception as e:
                print(f"Error processing chunk {i}: {str(e)}")
                continue

        # Combine results
        combined_result = "\n".join(parsed_results)
        return combined_result if combined_result else "No relevant information found."
    
    except Exception as e:
        raise Exception(f"Error in Gemini analysis: {str(e)}")