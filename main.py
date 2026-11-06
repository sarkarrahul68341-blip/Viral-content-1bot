import os
import razorpay
import threading
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Credentials
TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
RAZORPAY_KEY_ID = "rzp_test_Twuy8rP25nQzlV"
RAZORPAY_KEY_SECRET = "PQAYNmZVrzPoPtRZPgR14FrK"

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

app = Flask(__name__)

# Package Details
PACKAGES = {
    "pkg_1": {"name": "01 CP Video and File", "price": 249},
    "pkg_2": {"name": "02 Rap & CP & Big File VD", "price": 89},
    "pkg_3": {"name": "03 Mom and Son Real Sex", "price": 45},
    "pkg_4": {"name": "04 Insta viral reels and sex", "price": 30},
    "pkg_5": {"name": "05 Ganga bath group join", "price": 199},
    "pkg_6": {"name": "06 CP Bath camera hidden", "price": 55},
    "pkg_7": {"name": "07 Pakistani girl real fuke", "price": 49},
    "pkg_8": {"name": "08 Sister and brother sex", "price": 30},
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🔑 01 CP Video and File --------- Rs.249", callback_data="pkg_1")],
        [InlineKeyboardButton("🔑 02 Rap & CP & Big File VD --------- Rs.89", callback_data="pkg_2")],
        [InlineKeyboardButton("🔑 03 Mom and Son Real Sex --------- Rs.45", callback_data="pkg_3")],
        [InlineKeyboardButton("🔞 04 Insta viral reels and sex --------- Rs.30", callback_data="pkg_4")],
        [InlineKeyboardButton("🔥 05 Ganga bath group join --------- Rs.199", callback_data="pkg_5")],
        [InlineKeyboardButton("🔥 06 CP Bath camera hidden --------- Rs.55", callback_data="pkg_6")],
        [InlineKeyboardButton("🔥 07 Pakistani girl real fuke --------- Rs.49", callback_data="pkg_7")],
        [InlineKeyboardButton("❤️ 08 Sister and brother sex --------- Rs.30", callback_data="pkg_8")],

        
