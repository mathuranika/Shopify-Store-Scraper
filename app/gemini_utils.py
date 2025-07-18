import os
import json
from typing import List, Dict
import google.generativeai as genai
from bs4 import BeautifulSoup

# Configure the Gemini API
genai.configure(api_key="GEMINI_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def parse_html_to_text(html: str) -> str:
    """Convert HTML content into readable text using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.decompose()

    # Extract visible text
    text = soup.get_text(separator="\n")

    # Clean up blank lines and strip whitespace
    lines = [line.strip() for line in text.splitlines()]
    text = "\n".join(line for line in lines if line)

    return text

def chunk_text(text: str, max_words: int = 500) -> List[str]:
    """Split long text into manageable chunks for Gemini."""
    words = text.split()
    chunks = [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]
    return chunks

def extract_json_from_gemini(response_text: str) -> Dict:
    """Try to parse JSON from Gemini response."""
    try:
        # Extract JSON substring if needed
        start = response_text.find("{")
        end = response_text.rfind("}") + 1
        if start != -1 and end != -1:
            json_str = response_text[start:end]
            return json.loads(json_str)
    except Exception as e:
        print("Failed to parse JSON:", e)

    return {}

def summarise_shopify_info(html: str) -> Dict:
    """Main pipeline to convert raw HTML into structured product info."""
    text = parse_html_to_text(html)
    chunks = chunk_text(text)

    prompt = """
You are an AI assistant that extracts structured product and website data from Shopify storefronts. 
Return the following information in clean JSON format:

{
  "store_name": "",
  "description": "",
  "categories": [],
  "top_products": [
    {
      "name": "",
      "price": "",
      "description": "",
      "category": "",
      "image": ""
    }
  ]
}

Only include information that is confidently available from the text.
Do not guess. No commentary — return only JSON.
"""

    full_response = ""
    for i, chunk in enumerate(chunks):
        response = model.generate_content(prompt + "\n\n" + chunk)
        full_response += response.text + "\n"

    summary = extract_json_from_gemini(full_response)
    return summary or {"error": "Could not extract valid JSON from Gemini response."}
