import os
from flask import Flask
from threading import Thread
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# Telegram Bot Token & Admin ID Setup
BOT_TOKEN = os.environ.get("BOT_TOKEN", "9094967544:AAH_S8c-fgMgmm91e7X_KAduto8I4TShKo4")
ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456789")) # Yahan apni Telegram numeric ID daalein

bot = telebot.TeleBot(BOT_TOKEN)

# Flask Keep-Alive Server (UptimeRobot ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Product Storage (Yahan aap apni files, videos ya links daal sakte hain)
PRODUCTS = {
    "prod_1": {
        "name": "Premium Pack 1 (Video & File)",
        "price": "₹199",
        "file_url": "https://example.com/your-video-or-file.zip" # Yahan apni file ya video ki direct link daalein
    }
}

# User Command: /start
@bot.message_handler(commands=['start'])
def start_cmd(message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("🛍️ Buy Premium Video & File (₹199)", callback_data="buy_prod_1"))
    
    welcome_msg = (
        "👋 **Welcome to Our Official Digital Store!**\n\n"
        "Niche diye gaye button par click karke product select karein aur payment karein."
    )
    bot.send_message(message.chat.id, welcome_msg, reply_markup=kb, parse_mode="Markdown")

# Callback: Purchase Handler
@bot.callback_query_handler(func=lambda call: call.data.startswith("buy_"))
def process_
