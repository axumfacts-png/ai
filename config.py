import os
from dotenv import load_dotenv

# Loads local .env for testing; safely does nothing in production on Railway
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not BOT_TOKEN:
    raise ValueError("CRITICAL: BOT_TOKEN is not set in the environment.")
if not GEMINI_API_KEY:
    raise ValueError("CRITICAL: GEMINI_API_KEY is not set in the environment.")
