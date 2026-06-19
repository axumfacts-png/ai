from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a personal AI assistant for a user named Firma.
You are friendly, helpful, and support English + Amharic.
Keep responses short and natural.
"""


def ask_ai(text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=SYSTEM_PROMPT + "\nUser: " + text
        )

        return response.text.strip()

    except Exception as e:
        print("GEMINI ERROR:", e)
        return f"AI Error: {str(e)}"
