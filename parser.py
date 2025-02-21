from typing import List, Dict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
import os
import time
import json


class ContentParser:
    def __init__(self):
        self.model = ChatGoogleGenerativeAI(
            model="gemini-pro", google_api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.template = """
        Extract specific information from the following content based on this description: {parse_description}

        Content to analyze:
        {content}

        Guidelines:
        1. Extract all projects mentioned in the content.
        2. For each project, provide the following details:
           - Name of the project
           - Description of the project
           - Technologies used (if mentioned)
        3. Return the extracted information in valid JSON format.
        4. Use the following structure: {{"data": [{{"name": "Project Name", "description": "Project Description", "technologies": ["Tech1", "Tech2"]}}]}}
        5. If no projects are found, return {{"data": []}}
        """

        self.prompt = ChatPromptTemplate.from_template(self.template)

    def parse(self, content: str, parse_description: str) -> Dict:
        """Parse content using the Gemini model"""
        chunks = self._split_content(content)
        results = []

        for i, chunk in enumerate(chunks):
            print(f"Chunk {i + 1} of {len(chunks)}:")
            print(chunk)
            print("-" * 50)

            response = self._process_chunk(chunk, parse_description)
            if response and response.get("data"):
                results.extend(response["data"])

        return {"data": results} if results else {"data": []}

    def _split_content(
        self, content: str, max_length: int = 6000, overlap: int = 200
    ) -> List[str]:
        """Split content into manageable chunks with overlap"""
        chunks = []
        start = 0
        while start < len(content):
            end = start + max_length
            chunks.append(content[start:end])
            start = end - overlap
        return chunks

    def _process_chunk(self, chunk: str, parse_description: str) -> Dict:
        """Process a single chunk of content"""
        time.sleep(1)  # Rate limiting
        chain = self.prompt | self.model
        response = chain.invoke(
            {"content": chunk, "parse_description": parse_description}
        )

        try:
            # Safely parse the response into a dictionary
            return json.loads(response.content)
        except json.JSONDecodeError:
            # If the response is not valid JSON, return an empty result
            return {"data": []}
