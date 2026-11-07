import os
import asyncio
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Telegram Application Build
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

# Server startup par initialize
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(telegram_app.initialize())

# Packages Mapping
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

# Message box ke niche permanent buttons (Reply Keyboard)
def get_reply_keyboard():
    return ReplyKeyboardMarkup([
        [
            KeyboardButton("🎬 Demo"),
            KeyboardButton("📢 Channel"),
            KeyboardButton("🛠 Support")
        ]
    ], resize_keyboard=True)

# Product selection menu (Inline Buttons)
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
    
    # ❤️❤️❤️ ke sath updated welcome text
    welcome_text = f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:"
    
    if update.message:
        await update.message.reply_text("👇 Menu options:", reply_markup=reply_kb)
        await update.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    elif update.callback_query:
        await update.callback_query.message.reply_text(
            welcome_text,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def handle_text_buttons(update: Update, context):
    text = update.message.text
    if text == "🎬 Demo":
        await update.message.reply_text("🎬 Yeh raha aapka demo content link:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
    elif text == "📢 Channel":
        await update.message.reply_text("📢 Hamara official channel join karein:\n\n🔗 https://t.me/+iLoNw5R4Qwk5MGI1")
    elif text == "🛠 Support":
        await update.message.reply_text("🛠 Kisi bhi madad ke liye yahan contact karein:\n\n🔗 https://t.me/your_support_username")

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        user = update.effective_user
        user_name = user.first_name if user and user.first_name else "User"
        reply_markup = get_main_menu_keyboard()
        
        await query.message.edit_text(
            f"❤️❤️❤️ Hello **{user_name}**! ✨\n\nWelcome to **All Max Content Bot**\n\nSelect a package below to purchase:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
        return

    if data in PACKAGES:
        pkg = PACKAGES[data
    
