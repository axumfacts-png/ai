import telebot
import logging
import os
from config import BOT_TOKEN
from ai import get_ai_response
from stt import transcribe_audio
from tts import generate_audio

# Configure logging to monitor the bot's health in the Railway dashboard
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize bot
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I am your AI assistant. Send me a text or voice message!")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_chat_action(message.chat.id, 'typing')
    reply_text = get_ai_response(message.text)
    bot.reply_to(message, reply_text)

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    bot.send_chat_action(message.chat.id, 'record_voice')
    
    # Define file paths using the chat ID for concurrency safety
    input_audio_path = f"user_voice_{message.chat.id}.ogg"
    output_audio_path = f"ai_reply_{message.chat.id}.ogg"
    
    try:
        # 1. Download the voice note from Telegram
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(input_audio_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # 2. Transcribe Audio -> Text
        user_text = transcribe_audio(input_audio_path)
        
        if not user_text.strip():
            bot.reply_to(message, "Sorry, I couldn't hear any words in that audio.")
            return

        # 3. Send Text to Gemini -> Get AI Text
        ai_reply_text = get_ai_response(user_text)

        # 4. Generate AI Text -> Audio
        audio_file_path = generate_audio(ai_reply_text, output_audio_path)

        # 5. Send Audio back to user
        if audio_file_path:
            with open(audio_file_path, 'rb') as audio:
                bot.send_voice(message.chat.id, audio)
        else:
            # Fallback if text-to-speech fails
            bot.reply_to(message, ai_reply_text)

    except Exception as e:
        logging.error(f"Voice pipeline error: {e}")
        bot.reply_to(message, "Something went wrong while processing your voice note.")
        
    finally:
        # 6. Clean up files to prevent storage overflow
        if os.path.exists(input_audio_path):
            os.remove(input_audio_path)
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)

if __name__ == '__main__':
    logging.info("Starting bot... wiping pending updates to prevent conflicts.")
    
    # FIX: 'request_timeout' removed to prevent TypeError.
    # 'skip_pending=True' ignores backlogged messages from during downtime.
    # 'timeout=60' maintains a healthy long-polling connection.
    bot.infinity_polling(skip_pending=True, timeout=60)
