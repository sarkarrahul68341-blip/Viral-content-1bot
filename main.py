import os
import threading
import asyncio
import razorpay
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

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Setup a dedicated background event loop for Telegram Bot
bot_loop = asyncio.new_event_loop()

def start_background_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_background_loop, args=(bot_loop,), daemon=True).start()

telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()
asyncio.run_coroutine_threadsafe(telegram_app.initialize(), bot_loop).result()

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
        if saved_photo:
            try:
                await update.callback_query.message.edit_media(media=InputMediaPhoto(media=saved_photo, caption=welcome_text, parse_mode="Markdown"), reply_markup=reply_markup)
                return
            except Exception:
                pass
        await update.callback_query.message.edit_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def set_photo_handler(update: Update, context):
    message = update.message
    photo_obj = None
    if message.photo:
        photo_obj = message.photo[-1]
    elif message.reply_to_message and message.reply_to_message.photo:
        photo_obj = message.reply_to
