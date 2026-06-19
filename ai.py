import google.generativeai as genai
import logging
from config import GEMINI_API_KEY

# 1. Configure securely using the correct, stable SDK
genai.configure(api_key=GEMINI_API_KEY)

# 2. Use the fastest, most stable model for chat interactions
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_response(prompt: str) -> str:
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"Gemini API Error: {e}")
        return "I'm having a bit of trouble connecting to my brain right now. Try again in a moment."
