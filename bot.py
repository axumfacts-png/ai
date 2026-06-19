import telebot
import os

from config import BOT_TOKEN
from ai import ask_ai
from stt import voice_to_text
from tts import text_to_voice

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


# 🔥 IMPORTANT: prevent Telegram conflict errors
bot.remove_webhook()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "👋 Hi!\n\n🎤 Send voice or text."
    )


@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    downloaded = bot.download_file(file_info.file_path)

    with open("voice.ogg", "wb") as f:
        f.write(downloaded)

    bot.send_chat_action(message.chat.id, "typing")

    text = voice_to_text("voice.ogg")
    reply = ask_ai(text)

    audio = text_to_voice(reply)

    bot.send_voice(message.chat.id, open(audio, "rb"))


@bot.message_handler(func=lambda m: True)
def handle_text(message):
    reply = ask_ai(message.text)
    bot.send_message(message.chat.id, reply)


print("🤖 Firma Personal Voice Assistant Running...")

bot.infinity_polling(
    skip_pending=True,
    timeout=30,
    long_polling_timeout=30
)
