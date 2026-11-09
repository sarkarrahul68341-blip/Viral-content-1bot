import os
import logging
from flask import Flask, send_file
from threading import Thread

# Logging setup
logging.basicConfig(level=logging.INFO)

# Flask web server setup
app = Flask(__name__)

@app.route('/')
def home():
    try:
        # Yeh root URL par seedha aapka pricing page (index.html) serve karega
        return send_file('index.html')
    except Exception as e:
        return "Telegram Bot Server is Running with Single-Message UI Update!"

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run_web_server)
    t.daemon = True
    t.start()

# --- Aapka Telegram Bot Code yahan aayega ---
# Agar aap python-telegram-bot ya pyTelegramBotAPI use kar rahe hain,
# toh apna bot polling / startup code yahan niche likh sakte hain.

if __name__ == '__main__':
    # Web server ko background mein start karne ke liye
    keep_alive()
    
    logging.info("Telegram Bot and Web Server are starting up...")
    
    # Example bot runner (agar aapka bot polling use karta hai):
    # from bot_module import bot
    # bot.infinity_polling()
    
