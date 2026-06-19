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
    
    input_audio_path = f"user_voice_{message.chat.id}.ogg"
    output_audio_path = f"ai_reply_{message.chat.id}.ogg"
    
    try:
        # 1. Download the voice note
        file_info = bot.get_file(message.voice.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open(input_audio_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # 2. Process Audio
        user_text = transcribe_audio(input_audio_path)
        
        if not user_text.strip():
            bot.reply_to(message, "Sorry, I couldn't hear any words in that audio.")
            return

        # 3. Get AI Response
        ai_reply_text = get_ai_response(user_text)

        # 4. Generate Voice
        audio_file_path = generate_audio(ai_reply_text, output_audio_path)

        # 5. Send Audio back
        if audio_file_path:
            with open(audio_file_path, 'rb') as audio:
                bot.send_voice(message.chat.id, audio)
        else:
            bot.reply_to(message, ai_reply_text)

    except Exception as e:
        logging.error(f"Voice pipeline error: {e}")
        bot.reply_to(message, "Something went wrong while processing your voice note.")
        
    finally:
        if os.path.exists(input_audio_path):
            os.remove(input_audio_path)
        if os.path.exists(output_audio_path):
            os.remove(output_audio_path)

if __name__ == '__main__':
    # This dummy line forces the build system to register a change
    print("FORCE_REDEPLOY_2026") 
    
    logging.info("Starting bot...")
    
    # Clean polling configuration
    bot.infinity_polling(skip_pending=True)
