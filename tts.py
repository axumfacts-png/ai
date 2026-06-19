from gtts import gTTS
import logging

def generate_audio(text: str, output_path: str = "reply.ogg") -> str:
    """Takes text, generates an audio file, and returns the path to that file."""
    try:
        logging.info("Generating audio response...")
        tts = gTTS(text=text, lang='en', slow=False)
        tts.save(output_path)
        return output_path
    except Exception as e:
        logging.error(f"gTTS Error: {e}")
        return ""
