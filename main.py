import os
import subprocess
import sys
import traceback

# Automatic library installation check
try:
  import telegram
  import flask
except ImportError:
  subprocess.check_call([
      sys.executable,
      "-m",
      "pip",
      "install",
      "python-telegram-bot",
      "flask",
  ])

import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

# --- 1. APNI DETAILS YAHAN SET HAI ---
BOT_TOKEN = "9094967544:AAHk7zir2JbhHAQStB6BtcMFai4HbvwHQOQ"
UPI_ID = "puja6489@ptyes"
SUPPORT_TELEGRAM_LINK = "https://t.me/YourSupportUsername"

# --- 2. WELCOME BANNER PHOTO AUR TEXT ---
WELCOME_PHOTO_URL = "https://picsum.photos/800/500"
WELCOME_HEADING = "hello everyone ❤️❤️❤️\n\nWelcome to my official store! Niche diye gaye menu se content choose karein:"

# --- 3. PAID CONTENT DATABASE ---
CONTENT_DATABASE = {
    "item_1": {
        "title": "🔥 Premium Video Package 1",
        "price": "₹199",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
        "type": "video",
    },
    "item_2": {
        "title": "💎 Exclusive Photo Collection",
        "price": "₹99",
        "media_url": "https://picsum.photos/600/400",
        "type": "photo",
    },
}

# --- 4. FREE DEMO VIDEOS ---
DEMO_VIDEOS = {
    "demo_1": {
        "title": "🎬 Demo Video 1",
        "media_url": "https://raw.githubusercontent.com/sarkarrahul/Viral-content-1bot/main/FB_VID_3185228273639306254.mp4",
    },
    "demo_2": {
        "title": "🎬 Demo Video 2",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_3": {
        "title": "🎬 Demo Video 3",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_4": {
        "title": "🎬 Demo Video 4",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_5": {
        "title": "🎬 Demo Video 5",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_6": {
        "title": "🎬 Demo Video 6",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_7": {
        "title": "🎬 Demo Video 7",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_8": {
        "title": "🎬 Demo Video 8",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_9": {
        "title": "🎬 Demo Video 9",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
    "demo_10": {
        "title": "🎬 Demo Video 10",
        "media_url": "https://www.w3schools.com/html/mov_bbb.mp4",
    },
}

# --- 5. RENDER KEEP-ALIVE SERVER (Flask) ---
app_web = Flask(__name__)


@app_web.route("/")
def home():
  return "Bot is running live 24/7!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app_web.run(host="0.0.0.0", port=port)


# Telegram Bot Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  keyboard = []
  for key, data in CONTENT_DATABASE.items():
    keyboard.append([
        InlineKeyboardButton(
            f"{data['title']} — {data['price']}", callback_data=f"buy_{key}"
        )
    ])
  keyboard.append([
      InlineKeyboardButton("🎥 Watch Free Demo
