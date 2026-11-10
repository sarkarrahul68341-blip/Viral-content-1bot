import os
import asyncio
import qrcode
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# ==================== CONFIGURATION ====================
TELEGRAM_BOT_TOKEN = "9094967544:AAGu8LW9_3oXiBwww8jfBvlWvcnS4Ok4NWs"
UPI_ID = "Puja6489@ptyes"
BUSINESS_NAME = "All Max Content Bot"

# Aapke diye gaye naye links yahan set kar diye gaye hain:
DEMO_LINK = "https://t.me/+w4MJrYfZ2zIyMTQ1"
SUPPORT_LINK = "https://t.me/+T_Rwn6XiNPsyMDg9"

# Welcome Banner Photo ka Link
WELCOME_PHOTO_URL = "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe"

app = Flask(__name__)
telegram_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

# ==================== 8 PACKAGES CONFIGURATION ====================
PACKAGES = {
    "pkg_1": {"name": "🔑 01 Video and File", "price": 249, "link": "https://t.me/+iLoNw5R4Qwk5MGI1"},
    "pkg_2": {"name": "🔑 02 Rap & Big File VD", "price": 89, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_3": {"name": "🔑 03 Mom and Son Real Sex", "price": 45, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_4": {"name": "🔞 04 Insta viral reels and sex", "price": 30, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_5": {"name": "🔥 05 Ganga bath group join", "price": 199, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_6": {"name": "🔥 06 Bath camera hidden", "price": 55, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_7": {"name": "🔥 07 Pakistani girl real fuke", "price": 49, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
    "pkg_8": {"name": "❤️ 08 Sister and brother sex", "price": 30, "link": "https://t.me/+w4MJrYfZ2zIyMTQ1"},
}

# ==================== KEYBOARD FUNCTIONS ====================
def get_main_menu_keyboard():
    keyboard = []
    for key, pkg in PACKAGES.items():
        keyboard.append([InlineKeyboardButton(f"{pkg['name']} --------- Rs.{pkg['price']}", callback_data=key)])
    
    # Left Side: Demo Button | Right Side: Help/Support Button (Sath-sath)
    keyboard.append([
        InlineKeyboardButton("🚀 Free Demo", url=DEMO_LINK),
        InlineKeyboardButton("💬 Help / Support", url=SUPPORT_LINK)
    ])
    
    return InlineKeyboardMarkup(keyboard)

# ==================== QR CODE GENERATOR ====================
def generate_upi_qr(amount, pkg_name, order_id):
    upi_uri = f"upi://pay?pa={UPI_ID}&pn={BUSINESS_NAME}&am={amount}&cu=INR&tn=Order_{order_id}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(upi_uri)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    filename = f"qr_{order_id}.png"
    img.save(filename)
    return filename

# ==================== HANDLERS ====================
async def start(update: Update, context):
    reply_markup = get_main_menu_keyboard()
    caption = (
        "❤️ **Welcome to All Max Content Bot!** ❤️\n\n"
        "✨ Aapka yahan swagat hai! Niche diye gaye packages mein se apna pasandida option select karein:\n"
    )
    
    if update.callback_query:
        query = update.callback_query
        try:
            await query.message.delete()
        except Exception:
            pass
            
        await context.bot.send_photo(
            chat_id=query.message.chat_id,
            photo=WELCOME_PHOTO_URL,
            caption=caption,
            reply_markup=reply_markup,
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_photo(
            photo=WELCOME_PHOTO_URL,
            caption=caption,
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

    # 1. Package click karne par Sub-menu (Pay Now & Verify)
    if data in PACKAGES:
        pkg = PACKAGES[data]
        text = (
            f"📦 **{pkg['name']}**\n"
            f"💰 Price: **Rs.{pkg['price']}**\n\n"
            f"Aage badhne ke liye niche diye gaye option par click karein:"
        )
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("💳 Pay Now", callback_data=f"pay_{data}")],
            [InlineKeyboardButton("✅ Verify Payment", callback_data=f"verify_{data}")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ])
        
        try:
            if query.message.photo:
                await query.message.delete()
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=text,
                    reply_markup=keyboard,
                
