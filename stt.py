import whisper
import logging

# Load the model into memory ONCE at startup to prevent Railway CPU timeouts
logging.info("Loading Whisper model (this takes a few seconds)...")
try:
    model = whisper.load_model("base")
except Exception as e:
    logging.error(f"Failed to load Whisper model: {e}")

def transcribe_audio(file_path: str) -> str:
    """Takes an audio file path, returns the transcribed text."""
    try:
        logging.info(f"Transcribing {file_path}...")
        result = model.transcribe(file_path)
        return result["text"]
    except Exception as e:
        logging.error(f"Whisper Error: {e}")
        return ""
