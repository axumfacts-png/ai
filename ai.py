from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are a personal AI assistant for a user named Firma.

Rules:
- Be friendly and helpful.
- Support English and Amharic (አማርኛ).
- Keep answers concise unless the user asks for detail.
- Reply in the same language the user uses when possible.
- You are a personal assistant, not just a chatbot.
"""


def ask_ai(text: str) -> str:
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{SYSTEM_PROMPT}\n\nUser: {text}"
        )

        if response.text:
            return response.text.strip()

        return "Sorry Firma, I couldn't generate a response."

    except Exception as e:
        print("GEMINI ERROR:", str(e))
        return f"AI Error: {str(e)}"
