import telebot
from config import BOT_TOKEN
from ai import ask_ai
from stt import voice_to_text
from tts import text_to_voice

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# 👋 START (PERSONAL GREETING)
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Hi!!!\n\n🎤 Send voice or text."
    )


# 🎤 VOICE HANDLER
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open("voice.ogg", "wb") as f:
        f.write(downloaded)

    bot.send_chat_action(message.chat.id, "typing")

    # speech → text
    text = voice_to_text("voice.ogg")

    # AI response (personal + Amharic)
    reply = ask_ai(text)

    # text → voice
    audio = text_to_voice(reply)

    bot.send_voice(message.chat.id, open(audio, "rb"))


# 💬 TEXT HANDLER
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    reply = ask_ai(message.text)
    bot.send_message(message.chat.id, reply)


print("🤖 Firma Personal Voice Assistant Running...")
bot.infinity_polling(skip_pending=True)
