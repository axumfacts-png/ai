import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are a personal AI assistant for Firma.
Be helpful, friendly, and support English + Amharic.
Keep responses short.
"""

def ask_ai(text: str) -> str:
    try:
        response = model.generate_content(
            SYSTEM_PROMPT + "\nUser: " + text
        )
        return response.text.strip()

    except Exception as e:
        print("GEMINI ERROR:", e)
        return f"AI Error: {str(e)}"
