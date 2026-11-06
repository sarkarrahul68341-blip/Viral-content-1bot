import os
import subprocess
import sys
import traceback

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

# --- CONFIGURATIONS ---
BOT_TOKEN = "9094967544:AAHk7zir2JbhHAQStB6BtcMFai4HbvwHQOQ"
UPI_ID = "puja6489@ptyes"
SUPPORT_TELEGRAM_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"

# Yahan aapki nayi photo ka GitHub raw link set kar diya gaya hai
WELCOME_PHOTO_URL = "https://raw.githubusercontent.com/sarkarrahul/Viral-content-1bot/main/Indian-GF-Videos-porn-site.jpg"

WELCOME_HEADING = (
    "❤️ Welcome to Viral Desi MMS Content Bot ❤️\n\nNiche diye gaye menu se"
    " apna pasandida package ya demo select karein:"
)

# --- 8 PAID CONTENT PACKAGES DATABASE ---
CONTENT_DATABASE = {
    "item_1": {
        "title": "🔑 01 CP Video and File",
        "price": "Rs.249",
    },
    "item_2": {
        "title": "🔑 02 Rap & CP & Big File VD",
        "price": "Rs.89",
    },
    "item_3": {
        "title": "🔑 03 Mom and son Real sex",
        "price": "Rs.45",
    },
    "item_4": {
        "title": "🔞 04 Insta viral reels and sex",
        "price": "Rs.30",
    },
    "item_5": {
        "title": "🔥 05 Ganga bath group join",
        "price": "Rs.199",
    },
    "item_6": {
        "title": "🔥 06 CP Bath camera hidden",
        "price": "Rs.55",
    },
    "item_7": {
        "title": "🔥 07 pakistani girl real fuke",
        "price": "Rs.49",
    },
    "item_8": {
        "title": "❤️ 08 sister and brother sex",
        "price": "Rs.30",
    },
}

# --- 4 DEMO LINKS (Watch Free Demo ke andar khulenge) ---
DEMO_DATABASE = {
    "demo_1": {
        "title": "🎥 Watch Free Demo 1",
        "url": "https://t.me/+f9i3BlsoUeZiZmY1",
    },
    "demo_2": {
        "title": "🎥 Watch Free Demo 2",
        "url": "https://t.me/+w4MJrYfZ2zIyMTQ1",
    },
    "demo_3": {
        "title": "🎥 Watch Free Demo 3",
        "url": "https://t.me/+v_jJUbh_U7M3OGQ1",
    },
    "demo_4": {
        "title": "🎥 Watch Free Demo 4",
        "url": "https://t.me/+s4Zzmwni59diNjU1",
    },
}

# --- RENDER KEEP-ALIVE SERVER ---
app_web = Flask(__name__)


@
