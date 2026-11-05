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
