from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a personal AI assistant for a user named Firma.
Be friendly and helpful.
Support English and Amharic.
"""

def ask_ai(text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=text
        )

        return response.text

    except Exception as e:
        print("GEMINI ERROR:", str(e))
        return f"AI Error: {str(e)}"
