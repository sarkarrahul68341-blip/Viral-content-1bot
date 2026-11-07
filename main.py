import os
import time
import threading
import asyncio
import razorpay
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Telegram Application Build
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

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

def get_main_menu_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔑 01 CP Video and File --------- Rs.249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & CP & Big File VD --------- Rs.89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta viral reels and sex --------- Rs.30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga bath group join --------- Rs.199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath camera hidden --------- Rs.55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani girl real fuke --------- Rs.49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister and brother sex --------- Rs.30", callback_data="pkg_8")],
    ])

async def start(update: Update, context):
    reply_markup = get_main_menu_keyboard()
    if update.callback_query:
        await update.callback_query.message.edit_text(
            "✨ **All Max Content Bot**\n\nSelect a package below to purchase:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            "✨ **All Max Content Bot**\n\nSelect a package below to purchase:",
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )

async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    data = query.data

    if data == "main_menu":
        await start(update, context)
        return

    if data in PACKAGES:
        pkg = PACKAGES[data]
        payment_url = pkg["payment_link"]

        keyboard = [
            [InlineKeyboardButton(f"Pay ₹{pkg['price']} Now", url=payment_url)],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.message.edit_text(
            f"📦 **{pkg['name']}**\n💰 Price: **Rs.{pkg['price']}**\n\nClick the button below to complete your payment:",
            reply
        
