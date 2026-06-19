from gtts import gTTS

def text_to_voice(text: str, filename="reply.mp3"):
    # gTTS supports Amharic (am)
    lang = "am" if any(char in text for char in "አበባሀለሰተነአ") else "en"

    tts = gTTS(text=text, lang=lang)
    tts.save(filename)

    return filename
