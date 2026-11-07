import os
import threading
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

PHOTO_FILE = "welcome_photo.txt"

def get_saved_photo():
    if os.path.exists(PHOTO_FILE):
        with open(PHOTO_FILE, "r") as f:
            return f.read().strip()
    return None

def save_photo_id(file_id):
    with open(PHOTO_FILE, "w") as f:
        f.write(file_id)

# Flask App for Render Health Check & Razorpay Webhook
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram Bot Server is Running!"

@app.route('/razorpay-webhook', methods=['POST'])
def razorpay_webhook():
    data = request.get_json()
    if data.get("event") == "payment_link.paid":
        payment_entity = data["payload"]["payment_link"]["entity"]
        notes = payment_entity.get("notes", {})
        telegram_id = notes.get("telegram_id")
        package_id = notes.get("package_id")
        
        PACKAGES = {
            "pkg_1": {"name": "01 CP Video and File", "content_link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
            "pkg_2": {"name": "02 Rap & CP & Big File VD", "content_link": ""},
            "pkg_3": {"name": "03 Mom and Son Real Sex", "content_link": ""},
            "pkg_4": {"name": "04 Insta viral reels and sex", "content_link": ""},
            "pkg_5": {"name": "05 Ganga bath group join", "content_link": ""},
            "pkg_6": {"name": "06 CP Bath camera hidden", "content_link": ""},
            "pkg_7": {"name": "07 Pakistani girl real fuke", "content_link": ""},
            "pkg_8": {"name": "08 Sister and brother sex", "content_link": ""},
        }
        
        if telegram_id and package_id in PACKAGES:
            pkg = PACKAGES[package_id]
            channel_link = pkg["content_link"]
            if channel_link:
                requests.post(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", json={
                    "chat_id": telegram_id,
                    "text": f"✅ **Payment Successful!**\n\nAapne **{pkg['name']}** purchase kar liya hai.\n\nNiche diye gaye link se content access karein:\n\n🔗 {channel_link}",
                    "parse_mode": "Markdown"
                })
    return "OK", 200

# Telegram Bot Handlers
PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249, "payment_link": "https://rzp.io/l/testlink", "content_link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30, "payment_link": "https://rzp.io/l/testlink", "content_link": ""},
}

def get_reply_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("🎬 Demo"), KeyboardButton("📢 Channel"), KeyboardButton("🛠 Support")]
    ], resize_keyboard=True)

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 01 CP Video - ₹249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & Big File - ₹89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom & Son - ₹45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta Viral - ₹30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga Bath - ₹199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath Hidden - ₹55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani Girl - ₹49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister & Brother - ₹30", callback_data="pkg_8")],
    ])

async def start(update: Update, context):
    user = update.effective_user
    user_name = user.first_name if user and user.first_name else "User"
    reply_markup = get_main_menu_keyboard()
    reply_kb = get_reply_keyboard()
    welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
    saved_photo = get_saved_photo()
    
    if update.message:
        await update.message.reply_text("👇 Menu options:", reply_markup=reply_kb)
        if saved_photo:
            try:
                await update.message.reply_photo(photo=saved_photo, caption=welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
                return
            except Exception:
                pass
        await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        if
            
