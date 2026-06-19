from faster_whisper import WhisperModel

model = WhisperModel("base")

def voice_to_text(file_path: str) -> str:
    segments, _ = model.transcribe(
        file_path,
        language=None  # auto-detect Amharic/English
    )

    text = " ".join([s.text for s in segments])
    return text.strip()
